import type { ReactElement } from "react";
import { Navigate, Route, Routes } from "react-router-dom";

import { useAuth } from "./features/auth/AuthContext";
import LoginPage from "./features/auth/LoginPage";
import RegisterPage from "./features/auth/RegisterPage";
import EditorPage from "./features/editor/EditorPage";
import NotebookListPage from "./features/notebooks/NotebookListPage";

function RequireAuth({ children }: { children: ReactElement }) {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return children;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route
        path="/"
        element={
          <RequireAuth>
            <NotebookListPage />
          </RequireAuth>
        }
      />
      <Route
        path="/notebooks/:id"
        element={
          <RequireAuth>
            <EditorPage />
          </RequireAuth>
        }
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
