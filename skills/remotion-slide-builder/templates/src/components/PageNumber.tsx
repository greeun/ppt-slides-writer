import React from "react";
import { colors, fontSize, spacing } from "../theme";

type PageNumberProps = {
  pageNumber?: number;
  totalPages?: number;
  dark?: boolean;
};

export const PageNumber: React.FC<PageNumberProps> = ({
  pageNumber,
  totalPages,
  dark = false,
}) => {
  if (pageNumber === undefined) return null;

  return (
    <div
      style={{
        position: "absolute",
        bottom: spacing.element,
        right: spacing.page,
        fontSize: fontSize.small,
        color: dark ? "rgba(248,250,252,0.4)" : colors.textLight,
      }}
    >
      {pageNumber}{totalPages ? ` / ${totalPages}` : ""}
    </div>
  );
};
