import { useNavigate, useLocation } from "react-router-dom";
import AppHeader from "@/components/AppHeader";
import { Breadcrumbs } from "@/components/Breadcrumbs";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Calendar, BookOpen, ArrowRight, ArrowLeft } from "lucide-react";

const BatchSelection = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // Get selected course from previous page
  const { course = "BN" } = location.state || {};
  console.log("[BatchSelection] Loaded with course:", course);

  const batches = [
    {
      id: "pre-2022",
      title: "Before 2022 Batch",
      subtitle: "Year-wise Curriculum",
      description: "Traditional 4-year program structure",
      icon: BookOpen,
      path: "/year",
      type: "year",
      value: 1
    },
    {
      id: "2022-onwards",
      title: "2022 Onwards Batch",
      subtitle: "Semester System",
      description: "8 semesters with updated syllabus",
      icon: Calendar,
      path: "/semester",
      type: "sem",
      value: 1
    }
  ];

  // Log when user clicks "Back to Courses"
  const handleBack = () => {
    console.log("[BatchSelection] Back to Courses clicked");
    navigate('/course');
  };

  // Log batch selection and navigation
  const handleBatchSelect = (batch: typeof batches[0]) => {
    console.log("[BatchSelection] Batch selected:", batch);
    console.log("[BatchSelection] Navigating to:", batch.path, "with state:", { course, type: batch.type, value: batch.value });
    navigate(batch.path, { state: { course, type: batch.type, value: batch.value } });
  };

  return (
    <div className="min-h-screen bg-gradient-hero">
      <AppHeader />
      <div className="container mx-auto px-4 pt-0 pb-6">
        <Breadcrumbs 
          items={[
            { label: "Select Batch" }
          ]} 
        />
        
        <div className="mt-3 mb-6 animate-fade-in">
          <Button
            variant="ghost"
            size="sm"
            onClick={handleBack}
            className="px-3 py-1  text-black text-sm font-semibold mb-5 border-[0.7px] border-black/20 shadow-nav  rounded-"
          >
            <ArrowLeft className="w-4 h-4 mr-1" />
            Back to Courses
          </Button>
          
          <h1 className="text-2xl md:text-3xl font-bold text-foreground mb-3">
            Select Your Batch Year
          </h1>
          <p className="text-muted-foreground">
            Choose your batch to access the appropriate curriculum structure
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto animate-fade-in">
          {batches.map((batch) => (
            <Card
              key={batch.id}
              className="p-6 hover:shadow-lg transition-all cursor-pointer bg-gradient-card border-border hover:border-primary group"
              onClick={() => handleBatchSelect(batch)}
            >
              <div className="flex items-start space-x-4">
                <div className="p-3 bg-primary/10 rounded-xl group-hover:bg-primary/20 transition-colors">
                  <batch.icon className="w-8 h-8 text-primary" />
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-bold text-foreground mb-1">
                    {batch.title}
                  </h3>
                  <p className="text-sm text-primary font-medium mb-2">
                    {batch.subtitle}
                  </p>
                  <p className="text-sm text-muted-foreground">
                    {batch.description}
                  </p>
                </div>
                <ArrowRight className="w-5 h-5 text-muted-foreground group-hover:text-primary transition-colors mt-1" />
              </div>
            </Card>
          ))}
        </div>

        <div className="mt-12 max-w-2xl mx-auto text-center animate-fade-in">
          <div className="p-6  rounded-xl  ">
            <h3 className="font-semibold text-foreground mb-2">Not sure which batch you belong to?</h3>
            <p className="text-sm text-muted-foreground">
              If you started your B.Sc Nursing program in 2022 or later, select "2022 Onwards Batch" for the semester system. 
              For batches that started before 2022, select "Before 2022 Batch" for the year-wise curriculum.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BatchSelection;

