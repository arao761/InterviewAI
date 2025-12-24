export default function SetupProgressBar({
  currentStep,
  totalSteps,
  progress,
}: {
  currentStep: number;
  totalSteps: number;
  progress: number;
}) {
  return (
    <div className="mb-8">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-sm font-semibold text-foreground">Progress</h2>
        <span className="text-xs text-muted-foreground">{currentStep} of {totalSteps}</span>
      </div>
      <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-primary to-accent transition-all duration-300"
          style={{ width: `${progress}%` }}
        ></div>
      </div>
    </div>
  );
}
