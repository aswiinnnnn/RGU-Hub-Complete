import { useState } from "react";
import { RecruitmentCard } from "@/components/RecruitmentCard";
import { Breadcrumbs } from "@/components/Breadcrumbs";
import { NoticeBar } from "@/components/NoticeBar";
import { Button } from "@/components/ui/button";
import { Briefcase, GraduationCap, Users } from "lucide-react";

// Mock data - in a real app, this would come from an API
const recruitmentData = [
  {
    id: 1,
    companyName: "Apollo Hospitals",
    position: "Staff Nurse",
    location: "Delhi",
    jobType: 'FT' as const,
    description: "Looking for dedicated nursing professionals to join our critical care unit. Excellent growth opportunities and comprehensive benefits package.",
    requirements: "BSc Nursing degree, valid nursing license, minimum 1 year experience preferred",
    salary: "₹25,000 - ₹35,000/month",
    deadline: "2025-02-15",
    applyLink: "https://example.com/apply",
    postedOn: "2025-01-20",
    branch: 'bsc-nursing' as const
  },
  {
    id: 2,
    companyName: "Fortis Healthcare",
    position: "Nursing Intern",
    location: "Mumbai",
    jobType: 'IN' as const,
    description: "6-month internship program for final year BSc Nursing students. Hands-on experience in various departments.",
    requirements: "Final year BSc Nursing student, good communication skills",
    salary: "₹8,000/month stipend",
    deadline: "2025-02-28",
    applyLink: "https://example.com/apply",
    postedOn: "2025-01-18",
    branch: 'bsc-nursing' as const
  },
  {
    id: 3,
    companyName: "Max Healthcare",
    position: "Physiotherapist",
    location: "Bangalore",
    jobType: 'FT' as const,
    description: "Join our rehabilitation center as a full-time physiotherapist. Work with diverse patient population.",
    requirements: "BSc Physiotherapy, BPT degree, registration with state council",
    salary: "₹30,000 - ₹40,000/month",
    deadline: "2025-01-10",
    applyLink: "https://example.com/apply",
    postedOn: "2024-12-20",
    branch: 'bsc-physiotherapy' as const
  },
  {
    id: 4,
    companyName: "Sports Injury Centre",
    position: "Junior Physiotherapist",
    location: "Chennai",
    jobType: 'PT' as const,
    description: "Part-time position for sports injury rehabilitation. Flexible hours, perfect for continuing education.",
    requirements: "BSc Physiotherapy degree, interest in sports medicine",
    salary: "₹15,000/month",
    deadline: "2025-03-01",
    applyLink: "https://example.com/apply",
    postedOn: "2025-01-22",
    branch: 'bsc-physiotherapy' as const
  },
  {
    id: 5,
    companyName: "AIIMS",
    position: "ICU Nurse",
    location: "New Delhi",
    jobType: 'FT' as const,
    description: "Critical care nursing position in India's premier medical institution. Excellent learning environment.",
    requirements: "BSc Nursing, ICU experience preferred, BLS certification",
    salary: "₹40,000 - ₹50,000/month",
    deadline: "2025-02-20",
    applyLink: "https://example.com/apply",
    postedOn: "2025-01-15",
    branch: 'bsc-nursing' as const
  }
];

const Recruitment = () => {
  const [filter, setFilter] = useState<'all' | 'bsc-nursing' | 'bsc-physiotherapy'>('all');

  const filteredJobs = recruitmentData.filter(job => {
    if (filter === 'all') return true;
    return job.branch === filter;
  });

  const activeJobsCount = filteredJobs.filter(job => new Date(job.deadline) >= new Date()).length;

  return (
    <div className="min-h-screen bg-gradient-hero">
      <NoticeBar />
      
      <div className="container mx-auto px-4 py-8">
        <Breadcrumbs 
          items={[
            { label: "Home", path: "/" },
            { label: "Recruitment" }
          ]} 
        />

        {/* Header */}
        <div className="text-center mb-8 animate-fade-in">
          <div className="inline-flex items-center justify-center p-3 bg-primary/10 rounded-2xl mb-4">
            <Briefcase className="w-10 h-10 text-primary" />
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-2">
            Recruitment Portal
          </h1>
          <p className="text-muted-foreground">
            Find placements and internship opportunities
          </p>
          <div className="mt-4 inline-flex items-center gap-2 px-4 py-2 bg-success/10 rounded-lg">
            <span className="w-2 h-2 bg-success rounded-full animate-pulse" />
            <span className="text-sm font-medium text-success">{activeJobsCount} Active Opportunities</span>
          </div>
        </div>

        {/* Filter Buttons */}
        <div className="flex flex-wrap justify-center gap-3 mb-8 animate-fade-in">
          <Button
            variant={filter === 'all' ? 'default' : 'outline'}
            onClick={() => setFilter('all')}
            className="gap-2"
          >
            <Users className="w-4 h-4" />
            All Branches
          </Button>
          <Button
            variant={filter === 'bsc-nursing' ? 'default' : 'outline'}
            onClick={() => setFilter('bsc-nursing')}
            className="gap-2"
          >
            <GraduationCap className="w-4 h-4" />
            BSc Nursing
          </Button>
          <Button
            variant={filter === 'bsc-physiotherapy' ? 'default' : 'outline'}
            onClick={() => setFilter('bsc-physiotherapy')}
            className="gap-2"
          >
            <GraduationCap className="w-4 h-4" />
            BSc Physiotherapy
          </Button>
        </div>

        {/* Job Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-fade-in">
          {filteredJobs.map(job => (
            <RecruitmentCard key={job.id} {...job} />
          ))}
        </div>

        {filteredJobs.length === 0 && (
          <div className="text-center py-12">
            <p className="text-muted-foreground">No opportunities found for the selected filter.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Recruitment;