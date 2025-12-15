import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Root of the repo (parent of site/scripts)
const repoRoot = path.resolve(__dirname, '../../');
const dishesContentDir = path.resolve(__dirname, '../src/content/dishes');
const dishesPublicDir = path.resolve(__dirname, '../public/dishes');
const tipsContentDir = path.resolve(__dirname, '../src/content/tips');
const tipsPublicDir = path.resolve(__dirname, '../public/tips');
const dishesDir = path.join(repoRoot, 'dishes');
const tipsDir = path.join(repoRoot, 'tips');
const placeholderPath = path.join(repoRoot, 'dishes/colombian/nacionales/img/chorizo-2314640_640.jpg');
const baseUrl = '/AI-Chef';

// Clean existing directories
try {
  if (fs.existsSync(dishesContentDir)) {
    fs.rmSync(dishesContentDir, { recursive: true, force: true });
  }
} catch (e) { console.warn('Warning: Could not clear dishesContentDir:', e.message); }

try {
  if (fs.existsSync(dishesPublicDir)) {
    fs.rmSync(dishesPublicDir, { recursive: true, force: true });
  }
} catch (e) { console.warn('Warning: Could not clear dishesPublicDir:', e.message); }

try {
  if (fs.existsSync(tipsContentDir)) {
    fs.rmSync(tipsContentDir, { recursive: true, force: true });
  }
} catch (e) { console.warn('Warning: Could not clear tipsContentDir:', e.message); }

try {
  if (fs.existsSync(tipsPublicDir)) {
    fs.rmSync(tipsPublicDir, { recursive: true, force: true });
  }
} catch (e) { console.warn('Warning: Could not clear tipsPublicDir:', e.message); }

// Create target directories
fs.mkdirSync(dishesContentDir, { recursive: true });
fs.mkdirSync(dishesPublicDir, { recursive: true });
fs.mkdirSync(tipsContentDir, { recursive: true });
fs.mkdirSync(tipsPublicDir, { recursive: true });

// Copy function - separates images and markdown
function copyDir(src, destContent, destPublic, relativePath = '') {
  if (!fs.existsSync(src)) return;

  if (!fs.existsSync(destContent)) {
    fs.mkdirSync(destContent, { recursive: true });
  }
  if (!fs.existsSync(destPublic)) {
    fs.mkdirSync(destPublic, { recursive: true });
  }

  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destContentPath = path.join(destContent, entry.name);
    const destPublicPath = path.join(destPublic, entry.name);
    const newRelativePath = relativePath ? `${relativePath}/${entry.name}` : entry.name;

    if (entry.isDirectory()) {
      copyDir(srcPath, destContentPath, destPublicPath, newRelativePath);
    } else if (entry.isFile()) {
      const isImage = /\.(jpg|jpeg|png|gif|webp|svg)$/i.test(entry.name);

      if (isImage) {
        // Copy images to public/ (NOT to src/content/)
        try {
          const buffer = fs.readFileSync(srcPath);
          const content = buffer.toString('utf8', 0, 100);

          if (content.startsWith('version https://git-lfs.github.com/spec/v1')) {
            console.log(`Replacing LFS pointer: ${entry.name}`);
            if (fs.existsSync(placeholderPath)) {
              fs.copyFileSync(placeholderPath, destPublicPath);
            } else {
              fs.copyFileSync(srcPath, destPublicPath);
            }
          } else {
            fs.copyFileSync(srcPath, destPublicPath);
          }
        } catch (e) {
          console.error(`Error processing image ${srcPath}:`, e);
        }
      } else if (entry.name.endsWith('.md')) {
        // Copy markdown to src/content/ with updated image paths
        let content = fs.readFileSync(srcPath, 'utf8');

        // Replace relative image paths with absolute paths to /public
        content = content.replace(/\]\((?!http|https|\/|#)([^)]+)\)/g, (match, imgPath) => {
          try {
            // Skip if it's a .md link
            if (imgPath.endsWith('.md')) {
              return match;
            }

            // Clean the path
            let cleanPath = imgPath.replace(/^\.\//, '');

            // Build the public URL
            const publicUrl = `${baseUrl}/dishes/${newRelativePath.replace(entry.name, '')}${cleanPath}`.replace(/\/+/g, '/');

            console.log(`  Rewriting image path: ${imgPath} -> ${publicUrl}`);
            return `](${publicUrl})`;
          } catch (e) {
            console.error(`Error rewriting path ${imgPath}:`, e);
            return match;
          }
        });

        fs.writeFileSync(destContentPath, content);
      }
    }
  }
}

// Clean existing content and public directories first
console.log('Cleaning existing directories...');
try {
  if (fs.existsSync(dishesContentDir)) {
    fs.rmSync(dishesContentDir, { recursive: true, force: true });
  }
} catch (e) { console.warn('Warning: Could not clear dishesContentDir:', e.message); }

try {
  if (fs.existsSync(tipsContentDir)) {
    fs.rmSync(tipsContentDir, { recursive: true, force: true });
  }
} catch (e) { console.warn('Warning: Could not clear tipsContentDir:', e.message); }

try {
  if (fs.existsSync(dishesPublicDir)) {
    fs.rmSync(dishesPublicDir, { recursive: true, force: true });
  }
} catch (e) { console.warn('Warning: Could not clear dishesPublicDir:', e.message); }

try {
  if (fs.existsSync(tipsPublicDir)) {
    fs.rmSync(tipsPublicDir, { recursive: true, force: true });
  }
} catch (e) { console.warn('Warning: Could not clear tipsPublicDir:', e.message); }

// Recreate directories
fs.mkdirSync(dishesContentDir, { recursive: true });
fs.mkdirSync(tipsContentDir, { recursive: true });
fs.mkdirSync(dishesPublicDir, { recursive: true });
fs.mkdirSync(tipsPublicDir, { recursive: true });

console.log('Copying dishes to site content and public...');
if (fs.existsSync(dishesDir)) {
  const entries = fs.readdirSync(dishesDir, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(dishesDir, entry.name);

    if (entry.isDirectory()) {
      console.log(`Copying ${entry.name}...`);
      copyDir(srcPath, path.join(dishesContentDir, entry.name), path.join(dishesPublicDir, entry.name), entry.name);
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      fs.copyFileSync(srcPath, path.join(dishesContentDir, entry.name));
    }
  }
} else {
  console.error(`Dishes directory not found at ${dishesDir}`);
}

console.log('Copying tips to site content and public...');
if (fs.existsSync(tipsDir)) {
  const entries = fs.readdirSync(tipsDir, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(tipsDir, entry.name);

    if (entry.isDirectory()) {
      console.log(`Copying ${entry.name}...`);
      copyDir(srcPath, path.join(tipsContentDir, entry.name), path.join(tipsPublicDir, entry.name), entry.name);
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      fs.copyFileSync(srcPath, path.join(tipsContentDir, entry.name));
    }
  }
} else {
  console.error(`Tips directory not found at ${tipsDir}`);
}

console.log('Done.');
