import type { NextConfig } from "next";

// === SourceCraft Sites configuration ===
// Используйте этот файл вместо next.config.ts для статической сборки под SourceCraft Sites.
// Команда: cp next.config.static.ts next.config.ts && bun run build
// После сборки в папке `out/` будет готовый статический сайт — загрузите её в репозиторий GitHub.

const nextConfig: NextConfig = {
  output: "export",
  images: { unoptimized: true },
  typescript: { ignoreBuildErrors: true },
  reactStrictMode: false,
  // SourceCraft Sites не поддерживает кастомные заголовки, убираем их
  trailingSlash: true,
};

export default nextConfig;
