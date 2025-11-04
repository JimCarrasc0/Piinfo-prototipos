import { Card } from "./ui/card";
import { TrendingUp, Flame, MessageSquare, Users, ExternalLink, RotateCcw } from "lucide-react";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { useState } from "react";

export function HotTopicsSection() {
  const [isLoading, setIsLoading] = useState(false);
  const [lastUpdated, setLastUpdated] = useState("hace 5 min");

  const handleReload = async () => {
    setIsLoading(true);
    // Simular recarga de datos
    await new Promise(resolve => setTimeout(resolve, 1000));
    setLastUpdated("ahora mismo");
    setIsLoading(false);
    
    // Después de 5 segundos, volver a mostrar "hace 5 min"
    setTimeout(() => {
      setLastUpdated("hace 5 min");
    }, 5000);
  };

  const hotTopics = [
    {
      id: 1,
      topic: "#RevolucionIA2024",
      category: "Tecnología",
      engagement: "2.4M",
      growth: "+145%",
      posts: "12.3K",
      trending: true,
      description: "Avances en IA y su impacto en diversas industrias"
    },
    {
      id: 2,
      topic: "#VidaSostenible",
      category: "Estilo de Vida", 
      engagement: "1.8M",
      growth: "+89%",
      posts: "8.7K",
      trending: true,
      description: "Prácticas eco-amigables y elecciones de vida sostenible"
    },
    {
      id: 3,
      topic: "#TrabajoRemotoTips",
      category: "Negocios",
      engagement: "1.2M",
      growth: "+67%",
      posts: "5.4K",
      trending: false,
      description: "Consejos de productividad y bienestar para trabajadores remotos"
    },
    {
      id: 4,
      topic: "#SaludMentalConciencia",
      category: "Salud",
      engagement: "3.1M",
      growth: "+203%",
      posts: "15.8K",
      trending: true,
      description: "Apoyo e iniciativas de concienciación en salud mental"
    },
    {
      id: 5,
      topic: "#DetoxDigital",
      category: "Bienestar",
      engagement: "897K",
      growth: "+45%",
      posts: "3.2K",
      trending: false,
      description: "Tomar descansos de la tecnología para un mejor bienestar"
    },
    {
      id: 6,
      topic: "#EconomiaCreador", 
      category: "Negocios",
      engagement: "1.5M",
      growth: "+112%",
      posts: "7.1K",
      trending: true,
      description: "Monetizar contenido y construir negocios de creadores sostenibles"
    }
  ];

  const categoryColors = {
    "Tecnología": "bg-blue-500/20 text-blue-400 border-blue-500/30",
    "Estilo de Vida": "bg-green-500/20 text-green-400 border-green-500/30",
    "Negocios": "bg-purple-500/20 text-purple-400 border-purple-500/30",
    "Salud": "bg-red-500/20 text-red-400 border-red-500/30",
    "Bienestar": "bg-yellow-500/20 text-yellow-400 border-yellow-500/30"
  };

  return (
    <div className="mb-8">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-foreground">Temas Actuales</h2>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
            <Flame className="w-4 h-4 text-primary" />
            <span>Actualizado {lastUpdated}</span>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={handleReload}
            disabled={isLoading}
            className="flex items-center space-x-2"
          >
            <RotateCcw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
            <span className="hidden sm:inline">{isLoading ? 'Actualizando...' : 'Recargar'}</span>
          </Button>
        </div>
      </div>

      <div className="grid lg:grid-cols-2 xl:grid-cols-3 gap-4">
        {hotTopics.map((topic) => (
          <Card key={topic.id} className="p-4 bg-card border-border hover:bg-accent/50 transition-colors cursor-pointer group">
            <div className="space-y-3">
              {/* Header */}
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-2">
                  <h3 className="font-semibold text-foreground group-hover:text-primary transition-colors">
                    {topic.topic}
                  </h3>
                  {topic.trending && (
                    <TrendingUp className="w-4 h-4 text-primary" />
                  )}
                </div>
                <ExternalLink className="w-4 h-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>

              {/* Category Badge */}
              <Badge className={`${categoryColors[topic.category as keyof typeof categoryColors]} text-xs`}>
                {topic.category}
              </Badge>

              {/* Description */}
              <p className="text-sm text-muted-foreground line-clamp-2">
                {topic.description}
              </p>

              {/* Stats */}
              <div className="grid grid-cols-3 gap-2 pt-2 border-t border-border">
                <div className="text-center">
                  <div className="flex items-center justify-center mb-1">
                    <MessageSquare className="w-3 h-3 text-muted-foreground" />
                  </div>
                  <p className="text-xs font-medium text-foreground">{topic.engagement}</p>
                  <p className="text-xs text-muted-foreground">Engagement</p>
                </div>
                <div className="text-center">
                  <div className="flex items-center justify-center mb-1">
                    <TrendingUp className="w-3 h-3 text-green-400" />
                  </div>
                  <p className="text-xs font-medium text-green-400">{topic.growth}</p>
                  <p className="text-xs text-muted-foreground">Crecimiento</p>
                </div>
                <div className="text-center">
                  <div className="flex items-center justify-center mb-1">
                    <Users className="w-3 h-3 text-muted-foreground" />
                  </div>
                  <p className="text-xs font-medium text-foreground">{topic.posts}</p>
                  <p className="text-xs text-muted-foreground">Posts</p>
                </div>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}