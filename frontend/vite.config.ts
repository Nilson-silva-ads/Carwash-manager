import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa"; 


export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: "autoUpdate",
      includeAssets: ["pwa-192x192.png", "pwa-512x512.png"],
      manifest: {
        id: "/",
        name: "Carwash Manager",
        short_name: "Carwash",
        description: "Sistema de gerenciamento de serviços automotivos",
        lang: "pt-BR",
        theme_color: "#0f172a",
        background_color: "#ffffff",
        display: "standalone",
        start_url: "/",
        scope: "/",
        icons: [
          {
            src: "/pwa-192x192.png",
            sizes: "192x192",
            type: "image/png",
            purpose: "any"
          },
          {
            src: "/pwa-512x512.png",
            sizes: "512x512",
            type: "image/png",
            purpose: "any"
          },
          {
            src: "/pwa-512x512.png",
            sizes: "512x512",
            type: "image/png",
            purpose: "maskable"
          }
        ],
        screenshots: [
          {
            src: "/desktop.png",
            sizes: "1280x720",
            type: "image/png",
            form_factor: "wide",
            label: "Tela principal no Desktop"          
          },
          {
            src: "/mobile.png",
            sizes: "750x1334",
            type: "image/png",
            form_factor: "narrow",
            label: "Tela principal no Mobile"
          }

        ]
      },
    }),
  ],
});
