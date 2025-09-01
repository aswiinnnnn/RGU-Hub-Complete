import { useEffect } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";

// Navigates one step up according to breadcrumb logic when the user hits browser back
export const useBreadcrumbBack = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const params = useParams();

  useEffect(() => {
    let isNavigating = false;
    const handlePopState = (e: PopStateEvent) => {
      if (isNavigating) return;
      e.preventDefault();
      const path = location.pathname;
      const segments = path.split("/").filter(Boolean);

      // Default fallback
      let backPath = "/";

      // Map routes to their breadcrumb parent
      if (path === "/batch") backPath = "/";
      else if (path === "/year") backPath = "/batch";
      else if (path === "/semester") backPath = "/batch";
      else if (path.startsWith("/subjects/")) backPath = "/year";
      else if (path.startsWith("/semester-subjects/")) backPath = "/semester";
      else if (path.startsWith("/materials/")) backPath = `/subjects/${params.yearId ?? segments[1]}`;
      else if (path.startsWith("/semester-materials/")) backPath = `/semester-subjects/${params.semesterId ?? segments[1]}`;
      else if (path.startsWith("/download/")) backPath = `/materials/${params.yearId ?? segments[1]}/${params.subjectId ?? segments[2]}`;
      else if (path.startsWith("/semester-download/")) backPath = `/semester-materials/${params.semesterId ?? segments[1]}/${params.subjectId ?? segments[2]}`;
      else if (path.startsWith("/exam-session/")) {
        const type = segments[1];
        if (type === "year") backPath = `/materials/${params.yearId ?? segments[2]}/${params.subjectId ?? segments[3]}`;
        else backPath = `/semester-materials/${params.yearId ?? segments[2]}/${params.subjectId ?? segments[3]}`;
      }

      if (backPath === location.pathname) return;
      isNavigating = true;
      navigate(backPath, { replace: true });
      setTimeout(() => { isNavigating = false; }, 50);
    };

    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, [location.pathname, navigate, params]);
};

export default useBreadcrumbBack;


