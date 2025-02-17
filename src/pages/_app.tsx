import { CloudProvider } from "@/cloud/useCloud";
import { ToastProvider } from "@/components/toast/ToasterProvider";
import { ConfigProvider } from "@/hooks/useConfig";
import { ConnectionProvider } from "@/hooks/useConnection";
import "@livekit/components-styles/components/participant";
import "@/styles/globals.css";
import type { AppProps } from "next/app";

export default function App({ Component, pageProps }: AppProps) {
  return (
    <ToastProvider>
      <CloudProvider>
        <ConfigProvider>
          <ConnectionProvider>
            <Component {...pageProps} />
          </ConnectionProvider>
        </ConfigProvider>
      </CloudProvider>
    </ToastProvider>
  );
}