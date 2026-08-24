import { createContext, useContext, useMemo, useState, type ReactNode } from "react";

import { api, clearToken, getToken, setToken } from "../../api/client";

interface AuthState {
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthState | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setTokenState] = useState<string | null>(() => getToken());

  const value = useMemo<AuthState>(() => {
    const persist = (accessToken: string) => {
      setToken(accessToken);
      setTokenState(accessToken);
    };

    return {
      token,
      isAuthenticated: token !== null,
      login: async (email, password) => {
        const res = await api.post<{ access_token: string }>("/api/v1/auth/login", {
          email,
          password,
        });
        persist(res.access_token);
      },
      register: async (email, password) => {
        const res = await api.post<{ access_token: string }>("/api/v1/auth/register", {
          email,
          password,
        });
        persist(res.access_token);
      },
      logout: () => {
        clearToken();
        setTokenState(null);
      },
    };
  }, [token]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth deve ser usado dentro de AuthProvider");
  return ctx;
}
