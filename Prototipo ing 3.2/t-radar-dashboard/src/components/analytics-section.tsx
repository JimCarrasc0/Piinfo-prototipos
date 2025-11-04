import { Card } from "./ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from "recharts";

export function AnalyticsSection() {
  const weeklyData = [
    { name: 'Lun', posts: 4, engagement: 85, reach: 2400 },
    { name: 'Mar', posts: 3, engagement: 92, reach: 2800 },
    { name: 'Mié', posts: 5, engagement: 78, reach: 3200 },
    { name: 'Jue', posts: 2, engagement: 95, reach: 2100 },
    { name: 'Vie', posts: 6, engagement: 88, reach: 3800 },
    { name: 'Sáb', posts: 4, engagement: 91, reach: 4200 },
    { name: 'Dom', posts: 3, engagement: 87, reach: 3600 }
  ];

  const platformData = [
    { name: 'Instagram', value: 50, color: '#E4405F' },
    { name: 'Twitter', value: 30, color: '#1DA1F2' },
    { name: 'TikTok', value: 20, color: '#000000' }
  ];

  const metrics = [
    { label: 'Alcance Total', value: '124.5K', change: '+12.3%', positive: true },
    { label: 'Tasa de Engagement', value: '8.7%', change: '+2.1%', positive: true },
    { label: 'Nuevos Seguidores', value: '1,847', change: '+18.5%', positive: true },
    { label: 'Frecuencia de Posts', value: '4.2/día', change: '-0.3', positive: false }
  ];

  return (
    <div className="mb-8">
      <h2 className="text-xl font-semibold text-foreground mb-6">Tus Analíticas</h2>
      
      {/* Metrics Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {metrics.map((metric, index) => (
          <Card key={index} className="p-4 bg-card border-border">
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">{metric.label}</p>
              <p className="text-2xl font-semibold text-foreground">{metric.value}</p>
              <p className={`text-sm ${metric.positive ? 'text-green-400' : 'text-red-400'}`}>
                {metric.change}
              </p>
            </div>
          </Card>
        ))}
      </div>

      {/* Charts */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Engagement Chart */}
        <Card className="p-6 bg-card border-border">
          <h3 className="font-semibold text-foreground mb-4">Engagement Semanal</h3>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={weeklyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="name" stroke="#9CA3AF" />
              <YAxis stroke="#9CA3AF" />
              <Line 
                type="monotone" 
                dataKey="engagement" 
                stroke="#FF914D" 
                strokeWidth={2}
                dot={{ fill: '#FF914D', strokeWidth: 2, r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </Card>

        {/* Platform Distribution */}
        <Card className="p-6 bg-card border-border">
          <h3 className="font-semibold text-foreground mb-4">Distribución por Plataforma</h3>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={platformData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={80}
                fill="#FF914D"
              >
                {platformData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
          <div className="mt-4 space-y-2">
            {platformData.map((platform, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div 
                    className="w-3 h-3 rounded-full" 
                    style={{ backgroundColor: platform.color }}
                  ></div>
                  <span className="text-sm text-muted-foreground">{platform.name}</span>
                </div>
                <span className="text-sm font-medium text-foreground">{platform.value}%</span>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}