import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router";
import { AuthProvider } from "./app/AuthProvider";
import { AppRoutes } from "./app/router";
import { SeoManager } from "./app/SeoManager";
import { AssistantProvider } from "./features/assistant/AssistantProvider";
import "./shared/styles/tokens.css";
import "./shared/styles/base.css";
import "./shared/styles/content.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <SeoManager />
      <AuthProvider>
        <AssistantProvider>
          <AppRoutes />
        </AssistantProvider>
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>,
);
