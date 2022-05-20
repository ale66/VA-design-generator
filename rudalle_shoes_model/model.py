
from rudalle import get_rudalle_model, get_tokenizer, get_vae
from params import *
import torch
import multiprocessing
from psutil import virtual_memory
from dataset import *
from transformers import AdamW
import torch.nn.functional as F
from rudalle.dalle.utils import exists, is_empty
from einops import rearrange
from transformers import AdamW
from torch.utils.data import  DataLoader
from tqdm import tqdm
import matplotlib.pyplot as plt
import pickle
from functools import reduce 
import torch.nn.functional as F
from rudalle.dalle.utils import exists, is_empty
from einops import rearrange
ram_gb = round(virtual_memory().total / 1024**3, 1)

print("CPU:", multiprocessing.cpu_count())
print("RAM GB:", ram_gb)
print("PyTorch version:", torch.__version__)
print("CUDA version:", torch.version.cuda)
print("cuDNN version:", torch.backends.cudnn.version())
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("device:", device.type)


class Args:
    def __init__(self, epoch_amt, learning_rate):
        self.text_seq_length = model.get_param("text_seq_length")
        self.total_seq_length = model.get_param("total_seq_length")
        self.epochs = epoch_amt
        self.save_dir = "checkpoints"
        self.model_name = "lookingglass"
        self.save_every = 2000
        self.prefix_length = 10
        self.bs = 1
        self.clip = 0.24
        self.lr = learning_rate
        self.warmup_steps = 50
        self.wandb = False


model = get_rudalle_model("Malevich", pretrained=True, fp16=True, device=device)
vae = get_vae().to("cuda")
tokenizer = get_tokenizer()
torch_args = Args(epoch_amt, learning_rate)

st = RuDalleDataset(csv_path="data_desc.csv", tokenizer=tokenizer,model=model)
train_dataloader = DataLoader(
    st, batch_size=torch_args.bs, shuffle=True, drop_last=True
)

# Setup logs
torch_args.wandb = False

model.train()
optimizer = AdamW(model.parameters(), lr=torch_args.lr)

scheduler = torch.optim.lr_scheduler.OneCycleLR(
    optimizer,
    max_lr=torch_args.lr,
    final_div_factor=500,
    steps_per_epoch=len(train_dataloader),
    epochs=torch_args.epochs,
)

def freeze(
    model,
    freeze_emb=True,
    freeze_ln=False,
    freeze_attn=False,
    freeze_ff=True,
    freeze_other=True,
):
    for name, p in model.module.named_parameters():
        name = name.lower()
        if "ln" in name or "norm" in name:
            p.requires_grad = not freeze_ln
        elif "embeddings" in name:
            p.requires_grad = not freeze_emb
        elif "mlp" in name:
            p.requires_grad = not freeze_ff
        elif "attn" in name:
            p.requires_grad = not freeze_attn
        else:
            p.requires_grad = not freeze_other
    return model


class Layer(torch.nn.Module):
    def __init__(self, x, f, *args, **kwargs):
        super(Layer, self).__init__()
        self.x = x
        self.f = f
        self.args = args
        self.kwargs = kwargs

    def forward(self, x):
        return self.f(self.x(x, *self.args, **self.kwargs))


def _forward(
    self,
    input_ids,
    attention_mask,
    return_loss=False,
    use_cache=False,
    gradient_checkpointing=False,
):
    text = input_ids[:, : self.text_seq_length]
    text_range = torch.arange(self.text_seq_length)
    text_range += self.vocab_size - self.text_seq_length
    text_range = text_range.to(self.device)
    text = torch.where(text == 0, text_range, text)
    # some hardcode :)
    text = F.pad(text, (1, 0), value=2)
    text_embeddings = self.text_embeddings(text) + self.text_pos_embeddings(
        torch.arange(text.shape[1], device=self.device)
    )

    image_input_ids = input_ids[:, self.text_seq_length :]

    if exists(image_input_ids) and not is_empty(image_input_ids):
        image_embeddings = self.image_embeddings(
            image_input_ids
        ) + self.get_image_pos_embeddings(image_input_ids, past_length=0)
        embeddings = torch.cat((text_embeddings, image_embeddings), dim=1)
    else:
        embeddings = text_embeddings
    # some hardcode :)
    if embeddings.shape[1] > self.total_seq_length:
        embeddings = embeddings[:, :-1]

    alpha = 0.1
    embeddings = embeddings * alpha + embeddings.detach() * (1 - alpha)

    attention_mask = attention_mask[:, :, : embeddings.shape[1], : embeddings.shape[1]]
    t = self.transformer
    layers = []
    layernorms = []
    if not layernorms:
        norm_every = 0
    else:
        norm_every = len(t.layers) // len(layernorms)
    for i in range(len(t.layers)):
        layers.append(
            Layer(
                t.layers[i],
                lambda x: x[0] * layernorms[i // norm_every][0]
                + layernorms[i // norm_every][1]
                if norm_every and i % norm_every == 0
                else x[0],
                torch.mul(
                    attention_mask,
                    t._get_layer_mask(i)[
                        : attention_mask.size(2),
                        : attention_mask.size(3),
                    ],
                ),
                use_cache=False,
            )
        )
    if gradient_checkpointing:
        embeddings = torch.utils.checkpoint.checkpoint_sequential(layers, 6, embeddings)
        transformer_output = embeddings
        present_has_cache = False
    else:
        hidden_states = embeddings
        for i in range(len(t.layers)):
            mask = torch.mul(
                attention_mask,
                t._get_layer_mask(i)[
                    : attention_mask.size(2), : attention_mask.size(3)
                ],
            )
            hidden_states, present_has_cache = t.layers[i](
                hidden_states, mask, use_cache=use_cache
            )
        transformer_output = hidden_states
    transformer_output = self.transformer.final_layernorm(transformer_output)

    logits = self.to_logits(transformer_output)
    if return_loss is False:
        return logits, present_has_cache

    labels = torch.cat((text[:, 1:], image_input_ids), dim=1).contiguous().long()
    logits = rearrange(logits, "b n c -> b c n")

    text_logits = (
        logits[:, : self.vocab_size, : self.text_seq_length].contiguous().float()
    )
    image_logits = (
        logits[:, self.vocab_size :, self.text_seq_length :].contiguous().float()
    )

    loss_text = F.cross_entropy(text_logits, labels[:, : self.text_seq_length])
    loss_img = F.cross_entropy(image_logits, labels[:, self.text_seq_length :])

    loss = (loss_text + self.loss_img_weight * loss_img) / (self.loss_img_weight + 1)
    return loss, {"text": loss_text.data.detach().float(), "image": loss_img}


def train(model, input_files, args: Args, train_dataloader: RuDalleDataset):
    """
    args - arguments for training

    train_dataloader - RuDalleDataset class with text - image pair in batch
    """
    loss_logs = []
    try:
        progress = tqdm(
            total=(args.epochs * len(input_files)), desc="finetuning goes brrr"
        )
        save_counter = 0
        for epoch in range(args.epochs):
            print(epoch)
            for text, images in train_dataloader:
                device = model.get_param("device")
                save_counter += 1
                print(save_counter)
                print('model.zero_grad()')
                model.zero_grad()
                attention_mask = torch.tril(
                    torch.ones(
                        (args.bs, 1, args.total_seq_length, args.total_seq_length),
                        device=device,
                    )
                )
                image_input_ids = vae.get_codebook_indices(images)
                print('image input ids')
                print(image_input_ids)
                input_ids = torch.cat((text, image_input_ids), dim=1)
                _, loss = _forward(
                    model.module,
                    input_ids,
                    attention_mask.half(),
                    return_loss=True,
                    use_cache=False,
                    gradient_checkpointing=6,
                )
                loss = loss["image"]
                # train step
                print('loss.backward()')

                loss.backward()

                torch.nn.utils.clip_grad_norm_(model.parameters(), args.clip)
                optimizer.step()
                scheduler.step()
                print('optimizer.zero_grad()')
                optimizer.zero_grad()
                # save every here
                if save_counter % args.save_every == 0:
                    print(
                        f"Saving checkpoint here {args.model_name}_dalle_{save_counter}.pt"
                    )

                    plt.plot(loss_logs)
                    plt.show()
                    torch.save(
                        model.state_dict(),
                        os.path.join(
                            args.save_dir, f"{args.model_name}_dalle_{save_counter}.pt"
                        ),
                    )
                if args.wandb:
                    args.wandb.log({"loss": loss.item()})
                loss_logs += [loss.item()]
                progress.update()
                progress.set_postfix({"loss": loss.item()})

        print(f"Completly tuned and saved here  {args.model_name}__dalle_last.pt")

        with open('lossdata.pkl', 'wb') as f:
            pickle.dump(loss_logs, f)

        torch.save(
            model.state_dict(),
            os.path.join(args.save_dir, f"{args.model_name}_dalle_last.pt"),
        )

    except KeyboardInterrupt:
        print(
            f"What for did you stopped? Please change model_path to /{args.save_dir}/{args.model_name}_dalle_Failed_train.pt"
        )
        plt.plot(loss_logs)
        plt.show()

        torch.save(
            model.state_dict(),
            os.path.join(args.save_dir, f"{args.model_name}_dalle_Failed_train.pt"),
        )
    except Exception as err:
        print(f"Failed with {err}")
