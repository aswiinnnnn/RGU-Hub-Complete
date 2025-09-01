import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import BatchSelection from "./pages/BatchSelection";
import YearSelection from "./pages/YearSelection";
import SemesterSelection from "./pages/SemesterSelection";
import SubjectSelection from "./pages/SubjectSelection";
import SemesterSubjectSelection from "./pages/SemesterSubjectSelection";
import MaterialSelection from "./pages/MaterialSelection";
import SemesterMaterialSelection from "./pages/SemesterMaterialSelection";
import ExamSessionSelection from "./pages/ExamSessionSelection";
import DownloadPage from "./pages/DownloadPage";
import SemesterDownloadPage from "./pages/SemesterDownloadPage";
import NotFound from "./pages/NotFound";
import CourseSelection from "./pages/CourseSelection.tsx"; 

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} /> {/* Optional: redirect root to course selection */}
          <Route path="/course" element={<CourseSelection />} /> {/* Add this route */}
          <Route path="/batch" element={<BatchSelection />} />
          <Route path="/year" element={<YearSelection />} />
          <Route path="/semester" element={<SemesterSelection />} />
          <Route path="/subjects/:yearId" element={<SubjectSelection />} />
          <Route path="/semester-subjects/:semesterId" element={<SemesterSubjectSelection />} />
          <Route path="/materials/:yearId/:subjectId" element={<MaterialSelection />} />
          <Route path="/semester-materials/:semesterId/:subjectId" element={<SemesterMaterialSelection />} />
          <Route path="/exam-session/:type/:yearId/:subjectId/:materialType" element={<ExamSessionSelection />} />
          <Route path="/download/:yearId/:subjectId/:materialType" element={<DownloadPage />} />
          <Route path="/semester-download/:semesterId/:subjectId/:materialType" element={<SemesterDownloadPage />} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
