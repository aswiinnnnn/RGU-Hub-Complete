import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
// import { NoticeBar } from "@/components/NoticeBar";
import { PosterCarousel } from "@/components/PosterCarousel";
import AppHeader from "@/components/AppHeader";
import { HighlightCard } from "@/components/HighlightCard";
import { API_BASE_URL } from "@/config/api";
import { Button } from "@/components/ui/button";
import { 
  BookOpen, 
  FileText, 
  HelpCircle, 
  ClipboardList, 
  Stethoscope,
  GraduationCap,
  ArrowRight,
  Users,
  Download,
  BookMarked,
  Target,
  Briefcase
} from "lucide-react";

const Index = () => {
  const navigate = useNavigate();

  const highlights = [
    {
      icon: BookOpen,
      title: "Notes",
      description: "Subject-wise organized handouts",
      color: "primary"
    },
    {
      icon: FileText,
      title: "PYQ",
      description: "Previous Year University Question Papers",
      color: "accent"
    },
    {
      icon: HelpCircle,
      title: "Question Bank",
      description: "Unit-wise and chapter-wise",
      color: "success"
    },
    {
      icon: Stethoscope,
      title: "Practical Resources",
      description: "Clinical logbook, skill checklists, lab guides",
      color: "destructive"
    },
    {
      icon: ClipboardList,
      title: "Syllabus",
      description: "Year-wise syllabus (RGU/INC curriculum)",
      color: "secondary"
    },
    {
      icon: BookMarked,
      title: "Study Guides",
      description: "Comprehensive revision materials",
      color: "primary"
    }
  ];


  type LatestUpdate = {
    type: "Recruitment" | "Material";
    title: string;
    created_at: string;
  };

  const [latestUpdates, setLatestUpdates] = useState<LatestUpdate[]>([]);
  useEffect(() => {
    fetch(`${API_BASE_URL}/latest-updates/`)
      .then(res => {
        if (!res.ok) throw new Error(`Failed to load latest updates: ${res.status}`);
        return res.json();
      })
      .then(data => setLatestUpdates(data.results ?? data))
      .catch(() => {});
  }, []);



  return (
    <div className="min-h-screen bg-gradient-hero">
      {/* <NoticeBar /> */}
      {/* Header */}
      <AppHeader />
      
      {/* Poster Carousel */}
      <section className="container mx-auto px-4 pb-0">
        <PosterCarousel />
      </section>
      
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-12 md:py-20">
        <div className="text-center max-w-3xl mx-auto animate-fade-in">
          
          
          <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-4">
            RGU B.Sc Nursing 
            <span className="block text-primary mt-2">Study Hub</span>
          </h1>
          
          <p className="text-lg md:text-xl text-muted-foreground mb-8">
            Notes, PYQs & Question Banks for 2022–26 batch at one place
          </p>
          
          <Button 
            size="lg"
            onClick={() => navigate('/course')}
            className="bg-gradient-primary hover:opacity-90 text-primary-foreground px-8 py-6 text-lg rounded-xl shadow-medium"
          >
            Get Study Material
            <ArrowRight className="ml-2 w-5 h-5" />
          </Button>
        </div>
      </section>

      {/* Highlights Section */}
      <section className="container mx-auto px-4 ">
        <div className="text-center mb-10 animate-fade-in">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-3">
            Available Resources
          </h2>
          <p className="text-muted-foreground">
            Everything you need for your nursing education journey
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-fade-in">
          {highlights.map((item, index) => (
            <HighlightCard
              key={index}
              icon={item.icon}
              title={item.title}
              description={item.description}
              color={item.color}
              onClick={() => navigate('/course')}
            />
          ))}
        </div>
      </section>    

        {/* Recruitment Section */}
      <section className="container mx-auto px-4 pb-6 pt-12">
        <div className="max-w-4xl mx-auto">
          <div 
            onClick={() => navigate('/recruitment')}
            className="group bg-gradient-to-r from-primary/10 via-primary/5 to-success/10 hover:from-primary/20 hover:via-primary/10 hover:to-success/20 border border-primary rounded-2xl p-8 md:p-12 shadow-medium hover:shadow-lg transition-all duration-300 cursor-pointer animate-fade-in"
          >
            <div className="flex flex-col md:flex-row items-center gap-6">
              <div className="flex-shrink-0">
                <div className="p-4 bg-gradient-primary rounded-2xl shadow-medium group-hover:scale-110 transition-transform">
                  <Briefcase className="w-12 h-12 text-primary-foreground" />
                </div>
              </div>
              <div className="flex-1 text-center md:text-left">
                <h3 className="text-2xl md:text-3xl font-bold text-foreground mb-2">
                  Recruitment Portal
                </h3>
                <p className="text-muted-foreground mb-4">
                  Discover placement opportunities and internships for BSc Nursing & Physiotherapy students
                </p>
                <div className="inline-flex items-center gap-2 text-primary font-medium">
                  Browse Opportunities
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>


      {/* Latest Updates Section (API-driven) */}
      <section className="container mx-auto px-4 py-12">
        <div className="text-center mb-10 animate-fade-in">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-3">
            Latest Updates
          </h2>
          <p className="text-muted-foreground">
            Recently added and updated study materials & recruitments
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-4xl mx-auto animate-fade-in">
          {latestUpdates.map((item, idx) => {
            const isRecruitment = item.type === "Recruitment";
            const icon = isRecruitment ? <Briefcase className="w-6 h-6 text-success mr-2" /> : <BookOpen className="w-6 h-6 text-primary mr-2" />;
            const formattedDate = new Date(item.created_at).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
            return (
              <div
                key={idx}
                className="flex items-center bg-gradient-card rounded-xl p-4 border border-border shadow-sm cursor-pointer hover:shadow-md transition-all"
                onClick={() => {
                  if (isRecruitment) {
                    navigate('/recruitment');
                  } else {
                    // Without deep-link hints from backend, send user to the semester flow
                    navigate('/course');
                  }
                }}
              >
                {icon}
                <div className="flex-1">
                  <div className="font-semibold text-foreground text-lg mb-1">{item.title}</div>
                  <div className="text-xs text-muted-foreground">{isRecruitment ? "Recruitment" : "Material"} • {formattedDate}</div>
                </div>
              </div>
            );
          })}
        </div>
      </section>


       {/* About Section */}
       <section className="container mx-auto px-4 py-5 ">
        <div className="max-w-4xl mx-auto bg-gradient-card rounded-2xl p-8 md:p-12 border border-border shadow-medium animate-fade-in">
          <div className="flex items-center mb-6">
            <Users className="w-8 h-8 text-primary mr-3" />
            <h2 className="text-2xl md:text-3xl font-bold text-foreground">About RGU Hub</h2>
          </div>
          
          <p className="text-muted-foreground leading-relaxed">
            This platform is created for Rahul Gandhi University B.Sc Nursing students. The goal is to provide free, organized, and easy access to 
            notes, PYQs, question banks, syllabus, and practical resources. No login 
            required, just simple steps to get your study material.
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className=" border-t border-border mt-5">
        <div className="container mx-auto px-4 py-4">
          <div className="text-center space-y-2">
            <div className="flex items-center justify-center">
              <GraduationCap className="w-6 h-6 text-primary mr-2" />
              <span className="font-semibold text-foreground">RGU Hub</span>
            </div>
            
            <p className="text-sm text-muted-foreground">
              Copyright © 2025 RGU Hub
            </p>
            
            <div className="max-w-2xl mx-auto p-1 bg-mute rounded-lg">
              <p className="text-xs text-muted-foreground italic">
                <strong>Disclaimer:</strong> This is a platform made for students to access study materials easyil. 
                Official syllabus and results are available only on the official RGUHS website.
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
