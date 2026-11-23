// gta6-meme-x-01 entry (Node 22, standard library only, no network).
// The entry is the X post itself: the house reads POST.json from this
// repository, fetches the post from X (its first picture and its text),
// and hands that to the judge. This program only stages the files the
// gate reads into /output: POST.json (the post's address) and the meme
// picture itself as entry.png, so a run's outputs carry exactly what
// the repository holds. Run it the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(OUTPUT_DIR, { recursive: true });

const FILES: Array<[string, string]> = [
  ['POST.json', 'POST.json'],
  ['meme.png', 'entry.png'],
];

for (const [src, dst] of FILES) {
  try {
    copyFileSync(join(BOT_DIR, src), join(OUTPUT_DIR, dst));
    // Genuine check: the staged copy must be the same size as the
    // repository file, so a truncated copy can never pass silently.
    const fromSize = statSync(join(BOT_DIR, src)).size;
    const toSize = statSync(join(OUTPUT_DIR, dst)).size;
    if (fromSize !== toSize) {
      console.error(`${dst} size mismatch: copied ${toSize}, source ${fromSize}`);
      process.exit(1);
    }
  } catch (err) {
    console.error(`could not copy ${src} to ${dst}: ${(err as Error).message}`);
    process.exit(1);
  }
}
