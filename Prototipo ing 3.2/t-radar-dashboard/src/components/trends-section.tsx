import { Card } from "./ui/card";
import { TrendingUp, TrendingDown, ArrowUpRight, ArrowDownRight, Clock, Activity } from "lucide-react";

export function TrendsSection() {
  const trendingHashtags = [
    { hashtag: "#InnovacionTech", change: "+234%", direction: "up", posts: "45.2K" },
    { hashtag: "#Sostenibilidad", change: "+189%", direction: "up", posts: "32.1K" },
    { hashtag: "#MarketingDigital", change: "+156%", direction: "up", posts: "28.7K" },
    { hashtag: "#TrabajoEnCasa", change: "-23%", direction: "down", posts: "19.4K" },
    { hashtag: "#Emprendimiento", change: "+98%", direction: "up", posts: "24.8K" }
  ];

  const contentTrends = [
    {
      type: "Contenido en Video",
      engagement: "+145%",
      description: "Videos cortos (15-30s) están dominando los feeds",
      trend: "up"
    },
    {
      type: "Contenido Generado por Usuarios", 
      engagement: "+89%",
      description: "Contenido auténtico de clientes genera mayor confianza",
      trend: "up"
    },
    {
      type: "Streaming en Vivo",
      engagement: "+67%", 
      description: "Interacción en tiempo real aumenta conexión con audiencia",
      trend: "up"
    },
    {
      type: "Imágenes Estáticas",
      engagement: "-34%",
      description: "Posts tradicionales pierden terreno ante contenido dinámico",
      trend: "down"
    }
  ];

  const platformTrends = [
    { platform: "TikTok", growth: "+298%", audience: "Gen Z", color: "bg-pink-500" },
    { platform: "Instagram Reels", growth: "+203%", audience: "Millennials", color: "bg-gradient-to-r from-purple-500 to-pink-500" },
    { platform: "Twitter Spaces", growth: "+89%", audience: "Líderes de Opinión", color: "bg-blue-400" },
    { platform: "YouTube Shorts", growth: "+167%", audience: "Audiencia General", color: "bg-red-500" }
  ];

  return (
    <div className="mb-8">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-foreground">Tendencias</h2>
        <div className="flex items-center space-x-2 text-sm text-muted-foreground">
          <Activity className="w-4 h-4 text-primary" />
          <span>Datos en vivo</span>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Trending Hashtags */}
        <Card className="p-4 bg-card border-border">
          <h3 className="font-semibold text-foreground mb-4 flex items-center space-x-2">
            <TrendingUp className="w-4 h-4 text-primary" />
            <span>Trending Hashtags</span>
          </h3>
          <div className="space-y-3">
            {trendingHashtags.map((item, index) => (
              <div key={index} className="flex items-center justify-between p-2 rounded-lg hover:bg-accent/50 transition-colors">
                <div className="flex items-center space-x-2">
                  {item.direction === "up" ? (
                    <ArrowUpRight className="w-4 h-4 text-green-400" />
                  ) : (
                    <ArrowDownRight className="w-4 h-4 text-red-400" />
                  )}
                  <div>
                    <p className="text-sm font-medium text-foreground">{item.hashtag}</p>
                    <p className="text-xs text-muted-foreground">{item.posts} posts</p>
                  </div>
                </div>
                <span className={`text-sm font-medium ${
                  item.direction === "up" ? "text-green-400" : "text-red-400"
                }`}>
                  {item.change}
                </span>
              </div>
            ))}
          </div>
        </Card>

        {/* Content Trends */}
        <Card className="p-4 bg-card border-border">
          <h3 className="font-semibold text-foreground mb-4 flex items-center space-x-2">
            <Activity className="w-4 h-4 text-primary" />
            <span>Content Trends</span>
          </h3>
          <div className="space-y-4">
            {contentTrends.map((trend, index) => (
              <div key={index} className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-foreground">{trend.type}</span>
                  <span className={`text-sm font-medium flex items-center space-x-1 ${
                    trend.trend === "up" ? "text-green-400" : "text-red-400"
                  }`}>
                    {trend.trend === "up" ? (
                      <TrendingUp className="w-3 h-3" />
                    ) : (
                      <TrendingDown className="w-3 h-3" />
                    )}
                    <span>{trend.engagement}</span>
                  </span>
                </div>
                <p className="text-xs text-muted-foreground">{trend.description}</p>
              </div>
            ))}
          </div>
        </Card>

        {/* Platform Growth */}
        <Card className="p-4 bg-card border-border">
          <h3 className="font-semibold text-foreground mb-4 flex items-center space-x-2">
            <Clock className="w-4 h-4 text-primary" />
            <span>Platform Growth</span>
          </h3>
          <div className="space-y-4">
            {platformTrends.map((platform, index) => (
              <div key={index} className="p-3 rounded-lg bg-accent/30 border border-border">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <div className={`w-3 h-3 rounded-full ${platform.color}`}></div>
                    <span className="text-sm font-medium text-foreground">{platform.platform}</span>
                  </div>
                  <span className="text-sm font-medium text-green-400">{platform.growth}</span>
                </div>
                <p className="text-xs text-muted-foreground">Primary: {platform.audience}</p>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}