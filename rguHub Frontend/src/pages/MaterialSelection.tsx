import { useParams, useNavigate } from "react-router-dom";
import AppHeader from "@/components/AppHeader";
import useBreadcrumbBack from "@/hooks/use-breadcrumb-back";
import { Breadcrumbs } from "@/components/Breadcrumbs";
import { MaterialTypeCard } from "@/components/MaterialTypeCard";
import { subjects, years } from "@/data/academicData";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { 
  BookOpen, 
  FileText, 
  HelpCircle, 
  ClipboardList, 
  Stethoscope 
} from "lucide-react";

const MaterialSelection = () => {
  const { yearId, subjectId } = useParams();
  const navigate = useNavigate();
  useBreadcrumbBack();
  
  const yearNumber = parseInt(yearId || "1");
  const yearData = years[yearNumber - 1];
  const subject = subjects.find(s => s.id === subjectId);

  const materialTypes = [
    {
      title: "Notes",
      description: "Subject-wise organized handouts and study materials",
      icon: BookOpen,
      count: 12,
      color: "primary"
    },
    {
      title: "Previous Year Questions",
      description: "University question papers from past examinations",
      icon: FileText,
      count: 8,
      color: "accent"
    },
    {
      title: "Question Bank",
      description: "Unit-wise and chapter-wise practice questions",
      icon: HelpCircle,
      count: 15,
      color: "success"
    },
    {
      title: "Syllabus",
      description: "RGU/INC curriculum and course structure",
      icon: ClipboardList,
      count: 2,
      color: "secondary"
    },
    {
      title: "Practical Resources",
      description: "Clinical logbook, skill checklists, lab guides",
      icon: Stethoscope,
      count: 6,
      color: "primary"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-hero">
      <AppHeader />
      <div className="container mx-auto px-4 pt-0 pb-6">
        <Breadcrumbs 
          items={[
            { label: "Select Year", path: "/year" },
            { label: yearData?.year || "", path: `/subjects/${yearId}` },
            { label: subject?.name || "" }
          ]} 
        />
        
        <div className="mt-3 mb-6 animate-fade-in">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate(`/subjects/${yearId}`)}
            className="px-3 py-1  text-black text-sm font-semibold mb-5 border-[0.7px] border-black/20 shadow-nav  "
          >
            <ArrowLeft className="w-4 h-4 mr-1" />
            Back to Subjects
          </Button>
          
          <h1 className="text-2xl md:text-3xl font-bold text-foreground mb-3">
            {subject?.name}
          </h1>
          <p className="text-muted-foreground">
            Choose the type of material you want to access
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-fade-in">
          {materialTypes.map((type, index) => (
            <MaterialTypeCard
              key={index}
              icon={type.icon}
              title={type.title}
              description={type.description}
              count={type.count}
              color={type.color}
              onClick={() => {
                const materialTypeUrl = type.title.toLowerCase().replace(/ /g, '-');
                if (materialTypeUrl === 'previous-year-questions') {
                  navigate(`/exam-session/year/${yearId}/${subjectId}/${materialTypeUrl}`);
                } else {
                  navigate(`/download/${yearId}/${subjectId}/${materialTypeUrl}`);
                }
              }}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default MaterialSelection;