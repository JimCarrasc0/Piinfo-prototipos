import {
  Home,
  BarChart3,
  Users,
  TrendingUp,
  Calendar,
  Settings,
  Bell,
  MessageSquare,
  PlusCircle,
  Hash,
  Sun,
  Moon,
  ImageIcon,
} from "lucide-react";
import tradarIcon from '../imagenes/LOGO_APP_1080.png';
import { Switch } from "./ui/switch";
import { useState } from "react";

export function NavigationSidebar() {
  const [isDark, setIsDark] = useState(true);

  const toggleTheme = () => {
    setIsDark(!isDark);
    // Toggle the dark class on the html element
    document.documentElement.classList.toggle("dark");
  };

  const menuItems = [
    { icon: Home, label: "Panel", active: true },
    { icon: BarChart3, label: "Analíticas" },
    { icon: Users, label: "Audiencia" },
    { icon: MessageSquare, label: "Publicaciones" },
    { icon: Calendar, label: "Programar" },
    { icon: TrendingUp, label: "Tendencias" },
    { icon: Hash, label: "Hashtags" },
    { icon: Bell, label: "Notificaciones" },
    { icon: PlusCircle, label: "Crear" },
    { icon: Settings, label: "Configuración" },
  ];

  return (
    <div className="w-64 h-full bg-sidebar border-r border-sidebar-border p-4 flex flex-col">
      <div className="mb-8">
        <div className="flex items-center space-x-3 mb-2">
          <div className="w-8 h-8 bg-primary/10 border border-primary/20 rounded-lg flex items-center justify-center overflow-hidden rounded-[0px]">
            <img src={tradarIcon} alt="Icono T-Radar" className="w-8 h-8 object-contain" />
          </div>
          <h1 className="text-xl font-bold text-primary">
            T-Radar
          </h1>
        </div>
        <p className="text-sm text-muted-foreground ml-11">
          Gestiona tu presencia
        </p>
      </div>

      <nav className="flex-1">
        <ul className="space-y-2">
          {menuItems.map((item, index) => (
            <li key={index}>
              <a
                href="#"
                className={`flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
                  item.active
                    ? "bg-primary text-primary-foreground"
                    : "text-sidebar-foreground hover:bg-sidebar-accent"
                }`}
              >
                <item.icon className="w-5 h-5" />
                <span>{item.label}</span>
              </a>
            </li>
          ))}
        </ul>
      </nav>

      <div className="mt-auto pt-4 border-t border-sidebar-border space-y-4">
        {/* Theme Toggle */}
        <div className="flex items-center justify-between px-3 py-2">
          <div className="flex items-center space-x-2">
            {isDark ? (
              <Moon className="w-4 h-4 text-muted-foreground" />
            ) : (
              <Sun className="w-4 h-4 text-muted-foreground" />
            )}
            <span className="text-sm text-sidebar-foreground">
              {isDark ? "Modo Oscuro" : "Modo Claro"}
            </span>
          </div>
          <Switch
            checked={isDark}
            onCheckedChange={toggleTheme}
            className="data-[state=checked]:bg-primary"
          />
        </div>

        {/* User Info */}
        <div className="flex items-center space-x-3 px-3 py-2">
          <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
            <span className="text-sm font-medium text-primary-foreground">
              AA
            </span>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-sidebar-foreground truncate">
              Arturo Álvarez
            </p>
            <p className="text-xs text-muted-foreground truncate">
              r2d2.alvarez@mail.com
            </p>
            <p className="text-xs text-primary font-medium">
              Usuario Premium
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}