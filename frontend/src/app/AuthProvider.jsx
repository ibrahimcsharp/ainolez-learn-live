import { createContext, useContext, useEffect, useState } from "react";
import { api, refreshAccess, setAccessToken } from "../shared/api/client";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(false);

  // On page load, the refresh cookie (if any) restores the session.
  useEffect(() => {
    (async () => {
      if (await refreshAccess()) setUser(await api("/auth/me/").catch(() => null));
      setReady(true);
    })();
  }, []);

  async function login(email, password) {
    const data = await api("/auth/login/", { method: "POST", body: { email, password } });
    setAccessToken(data.access);
    setUser(data.user);
    return data.user;
  }

  async function logout() {
    await api("/auth/logout/", { method: "POST" }).catch(() => {});
    setAccessToken(null);
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, ready, login, logout, setUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);

export const homeFor = (user) => (user.role === "super_admin" ? "/admin" : "/dashboard");
