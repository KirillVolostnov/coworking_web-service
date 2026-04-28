import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import RoomCard from "../components/RoomCard";

describe("RoomCard", () => {
  it("renders room and handles click", () => {
    const onSelect = vi.fn();
    render(
      <RoomCard
        room={{
          id: 1,
          name: "Blue room",
          capacity: 6,
          photo_url: "https://example.com/blue.jpg"
        }}
        onSelect={onSelect}
      />
    );
    expect(screen.getByText("Blue room")).toBeInTheDocument();
    fireEvent.click(screen.getByText("Подробнее"));
    expect(onSelect).toHaveBeenCalled();
  });
});
