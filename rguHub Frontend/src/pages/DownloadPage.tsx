import { useParams, useNavigate } from "react-router-dom";
import { Breadcrumbs } from "@/components/Breadcrumbs";
import { DownloadCard } from "@/components/DownloadCard";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import AppHeader from "@/components/AppHeader";
import { useEffect, useState } from "react";
import { API_BASE_URL } from "@/config/api";
import useResponsiveToast from "@/hooks/use-toast";
import useBreadcrumbBack from "@/hooks/use-breadcrumb-back";
import { subjects, years } from "@/data/academicData";

const DownloadPage = () => {
  const { yearId, subjectId, materialType } = useParams();
  const navigate = useNavigate();
  const { show } = useResponsiveToast();
  useBreadcrumbBack();
  
  const yearNumber = parseInt(yearId || "1");
  const yearData = years[yearNumber - 1];
  const subject = subjects.find(s => s.id === subjectId);

  const [downloads, setDownloads] = useState([]);
  const [subjectName, setSubjectName] = useState("");

  useEffect(() => {
    if (!subjectId) return;
    fetch(`${API_BASE_URL}/materials/?subject=${subjectId}`)
      .then(res => res.json())
      .then(data => {
        setDownloads(data.results);
        if (data.length > 0) setSubjectName(data[0].subject?.name || "");
      });
  }, [subjectId]);

  const formatMaterialType = (type: string | undefined) => {
    return type?.replace(/-/g, ' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ') || '';
  };

  return (
    <div className="min-h-screen bg-gradient-hero">
      <AppHeader />
      <div className="container mx-auto px-4 pt-0 pb-6 ">
        <Breadcrumbs 
          items={[
            { label: "Select Year", path: "/year" },
            { label: yearData?.year || "", path: `/subjects/${yearId}` },
            { label: subjectName || "", path: `/materials/${yearId}/${subjectId}` },
            { label: formatMaterialType(materialType) }
          ]} 
        />
        
        <div className="mt-3 mb-6 animate-fade-in">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate(`/materials/${yearId}/${subjectId}`)}
            className="px-3 py-1  text-black text-sm font-semibold mb-5 border-[0.7px] border-black/20 shadow-nav  rounded-"
          >
            <ArrowLeft className="w-4 h-4 mr-1" />
            Back to Materials
          </Button>
          
          <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
            <div>
              <h1 className="text-2xl md:text-3xl font-bold text-foreground mb-2">
                {formatMaterialType(materialType)}
              </h1>
              <p className="text-muted-foreground">
                {subjectName} • {downloads.length} files available
              </p>
            </div>
          </div>
        </div>

        <div className="space-y-4 animate-fade-in">
          {downloads.map((download, index) => (
            <DownloadCard
              key={index}
              title={download.title}
              downloadUrl={download.url}
              uploadDate={download.created_at}
              type={download.type || "PDF"}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default DownloadPage;