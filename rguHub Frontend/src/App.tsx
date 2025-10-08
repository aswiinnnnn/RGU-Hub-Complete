/**
 * RGU Hub Frontend - Main Application Component
 * 
 * This is the root component of the RGU Hub React application. It sets up the
 * routing, global providers, and defines all application routes.
 * 
 * Features:
 * - React Router for client-side routing
 * - TanStack Query for API state management
 * - Toast notifications (Toaster + Sonner)
 * - Tooltip provider for UI components
 * 
 * Route Structure:
 * - /: Homepage with latest updates
 * - /course: Course selection (BSCN, BPT, etc.)
 * - /batch: Batch selection (2022-26, etc.)
 * - /year: Year selection (1st Year, 2nd Year, etc.)
 * - /semester: Semester selection (1st Sem, 2nd Sem, etc.)
 * - /subjects/:yearId: Subject selection for year-based programs
 * - /semester-subjects/:semesterId: Subject selection for semester-based programs
 * - /materials/:yearId/:subjectId: Material selection for year-based programs
 * - /semester-materials/:semesterId/:subjectId: Material selection for semester-based programs
 * - /download/:yearId/:subjectId/:materialType: Download page for year-based programs
 * - /semester-download/:semesterId/:subjectId/:materialType: Download page for semester-based programs
 * - /recruitment: Job postings and opportunities
 * - /*: 404 Not Found page
 * 
 * Author: RGU Hub Development Team
 * Last Updated: 2025
 */

import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";

// Page Components
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
import Recruitment from "./pages/Recruitment";

// Create TanStack Query client for API state management
const queryClient = new QueryClient();

/**
 * Main App Component
 * 
 * Sets up the application with all necessary providers and routing.
 * Uses React Router for navigation and TanStack Query for API state management.
 */
const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      {/* Toast notifications for user feedback */}
      <Toaster />
      <Sonner />
      
      <BrowserRouter>
        <Routes>
          {/* Homepage - Shows latest updates and program overview */}
          <Route path="/" element={<Index />} />
          
          {/* Course Selection - Choose between BSCN, BPT, etc. */}
          <Route path="/course" element={<CourseSelection />} />
          
          {/* Batch Selection - Choose academic batch (2022-26, etc.) */}
          <Route path="/batch" element={<BatchSelection />} />
          
          {/* Year Selection - Choose academic year (1st Year, 2nd Year, etc.) */}
          <Route path="/year" element={<YearSelection />} />
          
          {/* Semester Selection - Choose semester (1st Sem, 2nd Sem, etc.) */}
          <Route path="/semester" element={<SemesterSelection />} />
          
          {/* Subject Selection for Year-based Programs */}
          <Route path="/subjects/:yearId" element={<SubjectSelection />} />
          
          {/* Subject Selection for Semester-based Programs */}
          <Route path="/semester-subjects/:semesterId" element={<SemesterSubjectSelection />} />
          
          {/* Material Selection for Year-based Programs */}
          <Route path="/materials/:yearId/:subjectId" element={<MaterialSelection />} />
          
          {/* Material Selection for Semester-based Programs */}
          <Route path="/semester-materials/:semesterId/:subjectId" element={<SemesterMaterialSelection />} />
          
          {/* Exam Session Selection - Choose exam session for PYQs */}
          <Route path="/exam-session/:type/:yearId/:subjectId/:materialType" element={<ExamSessionSelection />} />
          
          {/* Download Page for Year-based Programs */}
          <Route path="/download/:yearId/:subjectId/:materialType" element={<DownloadPage />} />
          
          {/* Download Page for Semester-based Programs */}
          <Route path="/semester-download/:semesterId/:subjectId/:materialType" element={<SemesterDownloadPage />} />
          
          {/* Recruitment Portal - Job postings and opportunities */}
          <Route path="/recruitment" element={<Recruitment />} />
          
          {/* 404 Not Found - Must be last route */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
