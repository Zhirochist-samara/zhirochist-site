import type { Metadata } from "next";
import { Manrope } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";

const manrope = Manrope({
  variable: "--font-geist-sans",
  subsets: ["cyrillic", "latin"],
  weight: ["400", "500", "600", "700", "800"],
});

export const metadata: Metadata = {
  title: "ЖИРОЧИСТ Самара — чистка жироуловителей и канализации",
  description:
    "Самозанятый специалист по чистке жироуловителей и канализации в Самаре и пригороде. Выезд за 3 часа, документы для Роспотребнадзора, договорное обслуживание для общепита и производств.",
  keywords: [
    "чистка жироуловителей Самара",
    "обслуживание жироуловителей",
    "чистка канализации Самара",
    "жироуловитель обслуживание",
    "самозанятый Самара",
    "очистка жировых отходов",
    "ресторан Самара обслуживание",
  ],
  authors: [{ name: "ЖИРОЧИСТ Самара" }],
  openGraph: {
    title: "ЖИРОЧИСТ Самара — чистка жироуловителей и канализации",
    description:
      "Выезд за 3 часа. Документы для Роспотребнадзора. Договорное обслуживание для общепита и производств. Самара и пригороды.",
    siteName: "ЖИРОЧИСТ Самара",
    type: "website",
    locale: "ru_RU",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ru" suppressHydrationWarning>
      <body className={`${manrope.variable} antialiased bg-background text-foreground`}>
        {children}
        <Toaster />
      </body>
    </html>
  );
}
