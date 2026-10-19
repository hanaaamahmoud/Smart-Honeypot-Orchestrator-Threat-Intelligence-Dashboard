// // import { defineConfig } from 'vite'
// // import react from '@vitejs/plugin-react'

// // // https://vite.dev/config/
// // export default defineConfig({
// //   plugins: [react()],
// // })
// import { defineConfig } from "vite";
// import react from "@vitejs/plugin-react";

// export default defineConfig({
//   plugins: [react()],

//   server: {
//     port: 3000,
//     allowedHosts: ['navigator-throwback-playlist.ngrok-free.dev'],


//     proxy: {
//       "/backend": {
//         target: "http://localhost:8000",
//         changeOrigin: true,
//         secure: false,

//         rewrite: (path) =>
//           path.replace(/^\/backend/, ""),
//       },
//     },
//   },
// });

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],

  server: {
    port: 3000,

    allowedHosts: [
      "navigator-throwback-playlist.ngrok-free.dev",
    ],

    proxy: {
      "/backend": {
        target: "http://localhost:8000",
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/backend/, ""),
        ws: true,
      },
    },
  },
});