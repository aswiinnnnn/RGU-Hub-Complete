import { FC } from "react";
import { Link } from "react-router-dom";

export const AppHeader: FC = () => {
  return (
    <header className="sticky top-0 z-40 w-full bg-primary/70 backdrop-blur">
      <div className="container mx-auto px-4 h-14 flex items-center justify-start">
        <Link to="/" className="flex items-center gap-2" aria-label="Go to home">
          <img src="/favicon.ico" alt="RGU Hub logo" className="h-6 w-6 rounded-sm" />
          <span className="font-semibold text-foreground">RGU Hub</span>
        </Link>
      </div>
    </header>
  );
};

export default AppHeader;


