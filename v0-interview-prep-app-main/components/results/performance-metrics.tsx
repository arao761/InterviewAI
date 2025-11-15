import { Card } from '@/components/ui/card';

export default function PerformanceMetrics({ metrics }: { metrics: Record<string, number> }) {
  const metricsArray = [
    { label: 'Clarity', value: metrics.clarity, color: 'bg-blue-500' },
    { label: 'Confidence', value: metrics.confidence, color: 'bg-purple-500' },
    { label: 'Structure', value: metrics.structure, color: 'bg-cyan-500' },
    { label: 'Technical Accuracy', value: metrics.technicalAccuracy, color: 'bg-indigo-500' },
    { label: 'Engagement', value: metrics.engagement, color: 'bg-pink-500' },
  ];

  return (
    <Card className="bg-card border-border p-8">
      <h3 className="text-xl font-bold mb-6">Performance Metrics</h3>

      <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-6">
        {metricsArray.map((metric) => (
          <div key={metric.label} className="space-y-3">
            <div className="flex justify-between items-center">
              <p className="text-sm font-semibold text-foreground">{metric.label}</p>
              <p className="text-lg font-bold text-primary">{metric.value}%</p>
            </div>

            <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
              <div
                className={`h-full ${metric.color} transition-all duration-500`}
                style={{ width: `${metric.value}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}
