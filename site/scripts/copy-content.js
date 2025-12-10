import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Root of the repo (parent of site/scripts)
const repoRoot = path.resolve(__dirname, '../../');
const dishesContentDir = path.resolve(__dirname, '../src/content/dishes');
const tipsContentDir = path.resolve(__dirname, '../src/content/tips');
const dishesDir = path.join(repoRoot, 'dishes');
const tipsDir = path.join(repoRoot, 'tips');
const placeholderPath = path.join(repoRoot, 'dishes/colombian/nacionales/img/chorizo-2314640_640.jpg');

// Ensure target directories exist
if (fs.existsSync(dishesContentDir)) {
  fs.rmSync(dishesContentDir, { recursive: true, force: true });
}
fs.mkdirSync(dishesContentDir, { recursive: true });

if (fs.existsSync(tipsContentDir)) {
  fs.rmSync(tipsContentDir, { recursive: true, force: true });
}
fs.mkdirSync(tipsContentDir, { recursive: true });

// Copy function
function copyDir(src, dest) {
  if (!fs.existsSync(src)) return;
  
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }

  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else if (entry.isFile()) {
      const isImage = /\.(jpg|jpeg|png|gif|webp|svg)$/i.test(entry.name);
      if (isImage) {
        try {
          // Check for Git LFS pointer
          const buffer = fs.readFileSync(srcPath);
          const content = buffer.toString('utf8', 0, 100); // Read beginning
          if (content.startsWith('version https://git-lfs.github.com/spec/v1')) {
            console.log(`Replacing LFS pointer: ${entry.name}`);
            // It's an LFS pointer, use placeholder
            if (fs.existsSync(placeholderPath)) {
               fs.copyFileSync(placeholderPath, destPath);
            } else {
               // If placeholder missing, just copy original (will fail build likely, but best effort)
               fs.copyFileSync(srcPath, destPath);
            }
          } else {
            // Real image
            fs.copyFileSync(srcPath, destPath);
          }
        } catch (e) {
          console.error(`Error processing image ${srcPath}:`, e);
        }
      } else if (entry.name.endsWith('.md')) {
        // Read markdown content
        let content = fs.readFileSync(srcPath, 'utf8');
        
        // Fix relative image paths and ensure they exist
        content = content.replace(/\]\((?!http|https|\/)([^)]+)\)/g, (match, imgPath) => {
            // imgPath is like "img/foo.jpg" or "./img/foo.jpg"
            
            try {
              // Normalize path
              const targetPath = path.resolve(path.dirname(destPath), imgPath);
              
              // Check if it exists
              if (!fs.existsSync(targetPath)) {
                  console.log(`Missing image: ${imgPath} in ${entry.name}. Creating placeholder.`);
                  // Create directory if needed
                  fs.mkdirSync(path.dirname(targetPath), { recursive: true });
                  // Copy placeholder
                  if (fs.existsSync(placeholderPath)) {
                      fs.copyFileSync(placeholderPath, targetPath);
                  }
              }
              
              // Ensure it starts with ./ if it's relative
              if (!imgPath.startsWith('./') && !imgPath.startsWith('../')) {
                  return `](./${imgPath})`;
              }
            } catch (e) {
              console.error(`Error processing image path ${imgPath}:`, e);
            }
            return match;
        });
        
        fs.writeFileSync(destPath, content);
      }
    }
  }
}

console.log('Copying dishes to site content...');
if (fs.existsSync(dishesDir)) {
  const entries = fs.readdirSync(dishesDir, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(dishesDir, entry.name);
    const destPath = path.join(dishesContentDir, entry.name);
    
    if (entry.isDirectory()) {
      console.log(`Copying ${entry.name}...`);
      copyDir(srcPath, destPath);
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      fs.copyFileSync(srcPath, path.join(dishesContentDir, entry.name));
    }
  }
} else {
  console.error(`Dishes directory not found at ${dishesDir}`);
}

console.log('Copying tips to site content...');
if (fs.existsSync(tipsDir)) {
  const entries = fs.readdirSync(tipsDir, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(tipsDir, entry.name);
    const destPath = path.join(tipsContentDir, entry.name);
    
    if (entry.isDirectory()) {
      console.log(`Copying ${entry.name}...`);
      copyDir(srcPath, destPath);
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      fs.copyFileSync(srcPath, path.join(tipsContentDir, entry.name));
    }
  }
} else {
  console.error(`Tips directory not found at ${tipsDir}`);
}

console.log('Done.');
