import { Card } from "./ui/card";
import { TrendingUp, MessageSquare, Heart, Share, Eye, Clock } from "lucide-react";

export function RecentInsights() {
  const insights = [
    {
      id: 1,
      type: "engagement",
      title: "Hora Peak de Engagement Detectada",
      description: "Tu audiencia está más activa entre las 19:00-21:00",
      value: "+45%",
      change: "aumento",
      icon: TrendingUp,
      time: "hace 2 horas",
      color: "text-green-400"
    },
    {
      id: 2,
      type: "content",
      title: "Tipo de Contenido Más Exitoso",
      description: "Los videos están generando 3x más engagement",
      value: "3.2x",
      change: "multiplicador",
      icon: Eye,
      time: "hace 4 horas",
      color: "text-blue-400"
    },
    {
      id: 3,
      type: "audience",
      title: "Nuevo Segmento de Audiencia",
      description: "El grupo de 25-34 años muestra mayor interés",
      value: "+28%",
      change: "crecimiento",
      icon: Users,
      time: "hace 6 horas",
      color: "text-purple-400"
    },
    {
      id: 4,
      type: "hashtag",
      title: "Oportunidad de Hashtag Trending",
      description: "#TendenciasTech2024 está ganando impulso en tu nicho",
      value: "Hot",
      change: "trending",
      icon: Hash,
      time: "hace 8 horas",
      color: "text-primary"
    }
  ];

  return (
    <div className="mb-8">
      <h2 className="text-xl font-semibold text-foreground mb-6">Insights Recientes</h2>
      <div className="grid lg:grid-cols-2 gap-4">
        {insights.map((insight) => (
          <Card key={insight.id} className="p-4 bg-card border-border hover:bg-accent/50 transition-colors cursor-pointer">
            <div className="flex items-start justify-between">
              <div className="flex items-start space-x-3 flex-1">
                <div className="p-2 rounded-lg bg-accent">
                  <insight.icon className={`w-4 h-4 ${insight.color}`} />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium text-foreground mb-1">{insight.title}</h3>
                  <p className="text-sm text-muted-foreground mb-2">{insight.description}</p>
                  <div className="flex items-center space-x-4 text-xs text-muted-foreground">
                    <div className="flex items-center space-x-1">
                      <Clock className="w-3 h-3" />
                      <span>{insight.time}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div className={`text-right ${insight.color}`}>
                <div className="font-semibold">{insight.value}</div>
                <div className="text-xs opacity-75">{insight.change}</div>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

import { Users, Hash } from "lucide-react";