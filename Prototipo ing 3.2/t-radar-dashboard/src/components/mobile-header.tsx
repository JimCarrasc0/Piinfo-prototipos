import { useState } from "react";
import { Menu, MessageCircle, ImageIcon } from "lucide-react";
import { Button } from "./ui/button";
import { Sheet, SheetContent, SheetTrigger, SheetTitle, SheetDescription } from "./ui/sheet";
import { NavigationSidebar } from "./navigation-sidebar";
import { ChatbotSidebar } from "./chatbot-sidebar";
import tradarIcon from '../imagenes/LOGO_APP_1080.png';

export function MobileHeader() {
  const [leftOpen, setLeftOpen] = useState(false);
  const [rightOpen, setRightOpen] = useState(false);

  return (
    <div className="flex items-center justify-between px-4 py-3 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
      {/* Left Menu */}
      <Sheet open={leftOpen} onOpenChange={setLeftOpen}>
        <SheetTrigger asChild>
          <button className="lg:hidden -ml-2 inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-all disabled:pointer-events-none disabled:opacity-50 hover:bg-accent hover:text-accent-foreground dark:hover:bg-accent/50 size-9">
            <Menu className="w-5 h-5" />
            <span className="sr-only">Abrir menú de navegación</span>
          </button>
        </SheetTrigger>
        <SheetContent side="left" className="w-64 p-0 border-sidebar-border">
          <SheetTitle className="sr-only">Menú de Navegación</SheetTitle>
          <SheetDescription className="sr-only">Accede a todas las secciones del dashboard</SheetDescription>
          <div className="h-full overflow-hidden">
            <NavigationSidebar />
          </div>
        </SheetContent>
      </Sheet>

      {/* Center Title */}
      <div className="flex items-center space-x-2">
        <div className="w-6 h-6 bg-primary/10 border border-primary/20 rounded-md flex items-center justify-center overflow-hidden">
          <img src={tradarIcon} alt="T-Radar" className="w-4 h-4 object-contain" />
        </div>
        <div>
          <h1 className="text-base font-bold text-primary">T-Radar</h1>
        </div>
      </div>

      {/* Right Menu */}
      <Sheet open={rightOpen} onOpenChange={setRightOpen}>
        <SheetTrigger asChild>
          <button className="lg:hidden -mr-2 inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-all disabled:pointer-events-none disabled:opacity-50 hover:bg-accent hover:text-accent-foreground dark:hover:bg-accent/50 size-9">
            <MessageCircle className="w-5 h-5" />
            <span className="sr-only">Abrir BandurrIA</span>
          </button>
        </SheetTrigger>
        <SheetContent side="right" className="w-80 p-0 border-sidebar-border">
          <SheetTitle className="sr-only">BandurrIA - Asistente de IA</SheetTitle>
          <SheetDescription className="sr-only">Chat con tu asistente de IA para obtener sugerencias personalizadas</SheetDescription>
          <div className="h-full overflow-hidden">
            <ChatbotSidebar />
          </div>
        </SheetContent>
      </Sheet>
    </div>
  );
}