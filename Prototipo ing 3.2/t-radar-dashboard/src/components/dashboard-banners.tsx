import { TrendingUp, Users, ArrowRight } from "lucide-react";
import { Card } from "./ui/card";

export function DashboardBanners() {
  return (
    <div className="grid md:grid-cols-2 gap-6 mb-8">
      {/* Growth Banner */}
      <Card className="bg-gradient-to-r from-primary/20 to-primary/10 border-primary/20 p-6">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <div className="flex items-center space-x-2 mb-2">
              <TrendingUp className="w-5 h-5 text-primary" />
              <span className="text-sm font-medium text-primary">Alerta de Crecimiento</span>
            </div>
            <h3 className="text-lg font-semibold text-foreground mb-1">
              Tu alcance aumentó un 34%
            </h3>
            <p className="text-sm text-muted-foreground mb-4">
              ¡Buen trabajo! Tu contenido está funcionando excepcionalmente bien esta semana.
            </p>
            <div className="flex items-center space-x-1 text-primary hover:text-primary/80 cursor-pointer group">
              <span className="text-sm font-medium">Ver detalles</span>
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-primary">+34%</div>
            <div className="text-xs text-muted-foreground">vs semana pasada</div>
          </div>
        </div>
      </Card>

      {/* Audience Banner */}
      <Card className="bg-gradient-to-r from-blue-500/20 to-blue-500/10 border-blue-500/20 p-6">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <div className="flex items-center space-x-2 mb-2">
              <Users className="w-5 h-5 text-blue-400" />
              <span className="text-sm font-medium text-blue-400">Nuevo Hito</span>
            </div>
            <h3 className="text-lg font-semibold text-foreground mb-1">
              ¡10K seguidores alcanzados!
            </h3>
            <p className="text-sm text-muted-foreground mb-4">
              ¡Felicidades! Has alcanzado un hito importante. ¡Es hora de celebrar!
            </p>
            <div className="flex items-center space-x-1 text-blue-400 hover:text-blue-300 cursor-pointer group">
              <span className="text-sm font-medium">Compartir hito</span>
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-blue-400">10.2K</div>
            <div className="text-xs text-muted-foreground">seguidores totales</div>
          </div>
        </div>
      </Card>
    </div>
  );
}