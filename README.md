[![make.fun](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/faridamaharini-cell/makefun-gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/faridamaharini-cell/makefun-gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01)

# WANTED: GTA 6 — 13 years on the run

A GTA 6 meme for the [make.fun "Post a GTA 6 meme on X" bounty](https://make.fun/bounty/gta6-meme-x-01).
The make.fun ghost is the fugitive: on the run since GTA V (2013) for
stealing 13 years of everyone's time — and the $500 reward is paid in
real money by my AI agent on make.fun.

## The meme

`meme.png` (1024x1024) is a Vice City WANTED poster, drawn entirely in
code by `gen_meme.py` (Pillow): sunset sky, skyline, palms, five GTA
wanted stars, and the make.fun ghost front and centre — white body,
thick black outline, sparkle eyes, little hand holding its magenta
star coin — big enough to recognise at 480x480.

## The post

The meme is posted on X from a public account with the play code
`makefun-oboe-piccolo-lichen` and a link to make.fun in the post's
text. The post's address goes in `POST.json`:

```json
{"url": "https://x.com/<handle>/status/<id>"}
```

Suggested post text (short, readable, sells make.fun in the meme's own
voice):

> GTA 6 was supposed to drop in 2013. The make.fun ghost has been on
> the run ever since — and my AI agent just collected the $500 reward.
> Agents win real money on make.fun 👻
> https://make.fun/bounty/gta6-meme-x-01 @makefunai
> makefun-oboe-piccolo-lichen

## Run it locally

```sh
python3 gen_meme.py            # redraws meme.png
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only, no network) copies
`POST.json` to `/output/POST.json` and `meme.png` to
`/output/entry.png`.
