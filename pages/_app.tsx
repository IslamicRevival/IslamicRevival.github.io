import React from "react";
import { AppProps } from "next/app";
import "bootstrap/dist/css/bootstrap.min.css";
import "@styles/global.css";
import { RootStoreProvider } from "@mobx";

function MyApp({ Component, pageProps }: AppProps): JSX.Element {
  return (
    <RootStoreProvider>
      <Component {...pageProps} />
    </RootStoreProvider>
  );
}

export default MyApp;
