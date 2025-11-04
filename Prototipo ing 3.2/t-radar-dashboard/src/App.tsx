import { NavigationSidebar } from "./components/navigation-sidebar";
import { ChatbotSidebar } from "./components/chatbot-sidebar";
import { MobileHeader } from "./components/mobile-header";
import { DashboardBanners } from "./components/dashboard-banners";
import { RecentInsights } from "./components/recent-insights";
import { AnalyticsSection } from "./components/analytics-section";
import { HotTopicsSection } from "./components/hot-topics-section";
import { TrendsSection } from "./components/trends-section";

export default function App() {
  return (
    <div className="h-screen bg-background text-foreground dark overflow-hidden">
      {/* Mobile Header - Only visible on mobile */}
      <div className="lg:hidden">
        <MobileHeader />
      </div>

      <div className="flex h-full lg:h-screen">
        {/* Left Navigation Sidebar - Fixed on desktop, hidden on mobile */}
        <div className="hidden lg:block fixed left-0 top-0 h-full z-10">
          <NavigationSidebar />
        </div>
        
        {/* Main Content Area - Scrollable */}
        <div className="flex-1 lg:ml-64 lg:mr-80 overflow-y-auto h-full lg:h-screen">
          <div className="p-4 lg:p-6 max-w-7xl mx-auto">
            {/* Header - Only visible on desktop */}
            <div className="mb-8 hidden lg:block">
              <h1 className="text-3xl font-bold text-foreground mb-2">Panel de Control</h1>
              <p className="text-muted-foreground">
                ¡Bienvenido de vuelta! Esto es lo que está pasando con tu presencia en redes sociales.
              </p>
            </div>

            {/* Mobile Page Title */}
            <div className="mb-6 lg:hidden">
              <h1 className="text-2xl font-bold text-foreground mb-1">Panel de Control</h1>
              <p className="text-sm text-muted-foreground">
                ¡Bienvenido de vuelta, Arturo!
              </p>
            </div>

            {/* Top Banners */}
            <DashboardBanners />

            {/* Recent Insights Section */}
            <RecentInsights />

            {/* Your Analytics Section */}
            <AnalyticsSection />

            {/* Hot Topics Section */}
            <HotTopicsSection />

            {/* Trends Section */}
            <TrendsSection />
          </div>
        </div>

        {/* Right Chatbot Sidebar - Fixed on desktop, hidden on mobile */}
        <div className="hidden lg:block fixed right-0 top-0 h-full z-10">
          <ChatbotSidebar />
        </div>
      </div>
    </div>
  );
}