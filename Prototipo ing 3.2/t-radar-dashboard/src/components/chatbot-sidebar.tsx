import { MessageCircle, Send, Lightbulb, X } from "lucide-react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Card } from "./ui/card";

export function ChatbotSidebar() {
  const suggestions = [
    {
      id: 1,
      title: "Aumentar Engagement",
      description: "Publica en horarios pico (19:00-21:00) para mejor alcance",
      icon: TrendingUp
    },
    {
      id: 2,
      title: "Idea de Contenido",
      description: "Crea un video detrás de escenas de tu espacio de trabajo",
      icon: Lightbulb
    },
    {
      id: 3,
      title: "Estrategia de Hashtags",
      description: "Usa #MotivacionLunes con frases inspiradoras",
      icon: Hash
    }
  ];

  const chatMessages = [
    {
      id: 1,
      type: "bot",
      message: "¡Hola! Estoy aquí para ayudarte a hacer crecer tu presencia en redes sociales. ¿En qué te gustaría trabajar hoy?",
      time: "14:30"
    },
    {
      id: 2,
      type: "user", 
      message: "Necesito ideas para publicaciones de Instagram esta semana",
      time: "14:31"
    },
    {
      id: 3,
      type: "bot",
      message: "¡Excelente! Basándome en los datos de tu audiencia, aquí tienes algunas ideas de contenido trending que funcionarían bien para tu marca...",
      time: "14:31"
    }
  ];

  return (
    <div className="w-80 h-full bg-sidebar border-l border-sidebar-border flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-sidebar-border">
        <div className="flex items-center space-x-2">
          <MessageCircle className="w-5 h-5 text-primary" />
          <h2 className="font-semibold text-sidebar-foreground">BandurrIA</h2>
        </div>
        <p className="text-sm text-muted-foreground mt-1">Obtén sugerencias personalizadas</p>
      </div>

      {/* Suggestions */}
      <div className="p-4 border-b border-sidebar-border">
        <h3 className="text-sm font-medium text-sidebar-foreground mb-3">Ideas Rápidas</h3>
        <div className="space-y-2">
          {suggestions.map((suggestion) => (
            <Card key={suggestion.id} className="p-3 bg-sidebar-accent border-sidebar-border hover:bg-sidebar-accent/80 cursor-pointer transition-colors">
              <div className="flex items-start space-x-2">
                <Lightbulb className="w-4 h-4 text-primary mt-0.5 flex-shrink-0" />
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-sidebar-foreground">{suggestion.title}</p>
                  <p className="text-xs text-muted-foreground mt-1">{suggestion.description}</p>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 p-4 overflow-y-auto">
        <div className="space-y-4">
          {chatMessages.map((message) => (
            <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[80%] p-3 rounded-lg ${
                message.type === 'user' 
                  ? 'bg-primary text-primary-foreground' 
                  : 'bg-sidebar-accent text-sidebar-foreground'
              }`}>
                <p className="text-sm">{message.message}</p>
                <p className="text-xs opacity-70 mt-1">{message.time}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Chat Input */}
      <div className="p-4 border-t border-sidebar-border">
        <div className="flex space-x-2">
          <Input 
            placeholder="Pide sugerencias..." 
            className="flex-1 bg-sidebar-accent border-sidebar-border text-sidebar-foreground placeholder:text-muted-foreground"
          />
          <Button size="icon" className="bg-primary hover:bg-primary/90">
            <Send className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}

import { TrendingUp, Hash } from "lucide-react";