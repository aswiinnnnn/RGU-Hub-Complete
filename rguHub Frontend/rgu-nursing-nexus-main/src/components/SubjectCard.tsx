import { FileText, ChevronRight } from "lucide-react";

interface SubjectCardProps {
  name: string;
  onClick: () => void;
  materialCount?: number;
}

export const SubjectCard = ({ name, onClick, materialCount = 0 }: SubjectCardProps) => {
  return (
    <div 
      onClick={onClick}
      className="group bg-card hover:bg-card-hover border border-border rounded-xl p-5 shadow-soft hover:shadow-medium transition-all duration-300 cursor-pointer"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-start space-x-3 flex-1">
          <div className="p-2 bg-accent/10 rounded-lg group-hover:bg-accent/20 transition-colors">
            <FileText className="w-5 h-5 text-primary" />
          </div>
          <div className="flex-1">
            <h4 className="text-base font-semibold text-foreground leading-tight">{name}</h4>
            {materialCount > 0 && (
              <p className="text-xs text-muted-foreground mt-1">{materialCount} materials</p>
            )}
          </div>
        </div>
        <ChevronRight className="w-5 h-5 text-muted-foreground group-hover:text-primary transition-colors" />
      </div>
    </div>
  );
};