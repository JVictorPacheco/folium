import { useTheme } from "../features/theme/ThemeContext";

export default function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();
  return (
    <button
      className="icon-btn theme-toggle"
      onClick={toggleTheme}
      title={theme === "light" ? "Ativar tema escuro" : "Ativar tema claro"}
    >
      {theme === "light" ? "🌙" : "☀️"}
    </button>
  );
}
