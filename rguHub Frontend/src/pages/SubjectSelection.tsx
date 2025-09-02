import React, { useEffect, useState } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import AppHeader from "@/components/AppHeader";
import useBreadcrumbBack from "@/hooks/use-breadcrumb-back";
import { Breadcrumbs } from "@/components/Breadcrumbs";
import { SubjectCard } from "@/components/SubjectCard";
import { years } from "@/data/academicData";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { API_BASE_URL } from "@/config/api";

type Subject = {
  id: number;
  name: string;
  slug: string;
};

const SubjectSelection = () => {
  const { yearId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  useBreadcrumbBack();

  const { course = "bn", type = "year", value = yearId ? parseInt(yearId) : 1 } = location.state || {};

  console.log("Selected course:", course);
  console.log("Curriculum type:", type);
  console.log("Year/Sem value:", value);

  const yearNumber = type === "year" ? value : 1;
  const yearData = years[yearNumber - 1];

  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [loading, setLoading] = useState(true);
  

  useEffect(() => {
    const fetchSubjects = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/subjects/?course=${course}&sem=${value}`);
        const data = await res.json();
        // Ensure subjects is always an array
        setSubjects(Array.isArray(data) ? data : []);
      } catch (err) {
        console.error(err);
        setSubjects([]);
      } finally {
        setLoading(false);
      }
    };

    fetchSubjects();
  }, [course, value]);





  return (
    <div className="min-h-screen bg-gradient-hero">
      <AppHeader />
      <div className="container mx-auto px-4 pt-0 pb-6">
        <Breadcrumbs
          items={[
            { label: type === "year" ? "Select Year" : "Select Semester", path: type === "year" ? "/year" : "/semester" },
            { label: yearData?.year || "" },
          ]}
        />

        <div className="mt-3 mb-6 animate-fade-in">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate(type === "year" ? "/year" : "/semester")}
            className="px-3 py-1 text-black text-sm font-semibold mb-5 border-[0.7px] border-black/20 shadow-nav"
          >
            <ArrowLeft className="w-4 h-4 mr-1" />
            Back to {type === "year" ? "Years" : "Semesters"}
          </Button>

          <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-3">
            {type === "year" ? yearData?.year : `Semester ${value}`} Subjects
          </h1>
          <p className="text-muted-foreground">Select a subject to access study materials</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 animate-fade-in">
          {loading ? (
            <p className="text-muted-foreground">Loading subjects...</p>
          ) : Array.isArray(subjects) && subjects.length > 0 ? (
            subjects.map((subject) => (
              <SubjectCard
                key={subject.id}
                name={subject.name}
                materialCount={5}
                onClick={() =>
                  navigate(`/materials/${value}/${subject.slug}`, {
                    state: { course, type, value },
                  })
                }
              />
            ))
          ) : (
            <div className="col-span-2">
              <div className="text-center py-8">
                <div className="max-w-md mx-auto">
                  <div className="text-4xl mb-3">📄</div>
                  <h3 className="text-lg font-semibold text-foreground mb-2">No Subjects Found</h3>
                  <p className="text-muted-foreground mb-3">
                    Subjects for this course or term are not available.
                  </p>
                  <div className="bg-amber-50 border border-amber-200 rounded-lg p-3 mb-4">
                    <p className="text-amber-800 text-sm">
                      Contact admin to request updates for this course.
                    </p>
                  </div>
                  <Button
                    variant="outline"
                    onClick={() => navigate(type === "year" ? "/year" : "/semester")}
                  >
                    <ArrowLeft className="w-4 h-4 mr-1" />
                    Back to {type === "year" ? "Years" : "Semesters"}
                  </Button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SubjectSelection;
