import * as React from "react"
import { cn } from "@/lib/utils"

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "success" | "warning" | "error" | "outline"
}

function Badge({ className, variant = "default", ...props }: BadgeProps) {
  return (
    <div
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
        {
          "border-transparent bg-[var(--color-primary)]/20 text-[var(--color-primary)]": variant === "default",
          "border-transparent bg-[var(--color-success)]/20 text-[var(--color-success)]": variant === "success",
          "border-transparent bg-[var(--color-warning)]/20 text-[var(--color-warning)]": variant === "warning",
          "border-transparent bg-[var(--color-error)]/20 text-[var(--color-error)]": variant === "error",
          "text-foreground border-slate-700": variant === "outline",
        },
        className
      )}
      {...props}
    />
  )
}

export { Badge }
