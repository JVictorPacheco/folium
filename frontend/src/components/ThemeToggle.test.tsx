import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it } from "vitest";

import ThemeToggle from "./ThemeToggle";
import { ThemeProvider } from "../features/theme/ThemeContext";

describe("ThemeToggle", () => {
  beforeEach(() => localStorage.clear());

  it("alterna o título ao clicar (claro → escuro)", () => {
    render(
      <ThemeProvider>
        <ThemeToggle />
      </ThemeProvider>,
    );

    const button = screen.getByRole("button");
    expect(button).toHaveAttribute("title", "Ativar tema escuro");

    fireEvent.click(button);
    expect(button).toHaveAttribute("title", "Ativar tema claro");

    fireEvent.click(button);
    expect(button).toHaveAttribute("title", "Ativar tema escuro");
  });
});
