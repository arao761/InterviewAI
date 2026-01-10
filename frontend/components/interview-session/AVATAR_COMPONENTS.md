# Interview Avatar Components

This directory contains three different avatar components for the interview interface. Each provides a visual representation of the AI interviewer that animates when speaking.

## Components Overview

### 1. AnimatedFaceAvatar (Default - Currently Used)
**File:** `animated-face-avatar.tsx`

A friendly, cartoon-style animated face with eyes, mouth, and blinking animations.

**Features:**
- Realistic mouth movement synced with speech
- Random eye blinking for lifelike appearance
- Sound wave visualizations
- Smooth animations and transitions
- Works in both light and dark mode

**Usage:**
```tsx
import AnimatedFaceAvatar from '@/components/interview-session/animated-face-avatar';

<AnimatedFaceAvatar
  isSpeaking={aiSpeaking}
  name="AI Interviewer"
/>
```

**Props:**
- `isSpeaking` (boolean, required): Whether the AI is currently speaking
- `name` (string, optional): Display name for the avatar (default: "AI Interviewer")

**Best For:** Behavioral and mixed interviews where a friendly, approachable appearance is preferred.

---

### 2. TalkingAvatar
**File:** `talking-avatar.tsx`

A modern, gradient-based avatar with customizable style and size options.

**Features:**
- Circular or square avatar shapes
- Multiple size options (sm, md, lg, xl)
- Gradient background with pulse effects
- Real-time audio waveform visualization
- Ripple effects when speaking
- Speaking indicator badge

**Usage:**
```tsx
import TalkingAvatar from '@/components/interview-session/talking-avatar';

<TalkingAvatar
  isSpeaking={aiSpeaking}
  name="AI Interviewer"
  style="circle"
  size="lg"
/>
```

**Props:**
- `isSpeaking` (boolean, required): Whether the AI is currently speaking
- `name` (string, optional): Display name (default: "AI Interviewer")
- `style` ('circle' | 'square', optional): Avatar shape (default: 'circle')
- `size` ('sm' | 'md' | 'lg' | 'xl', optional): Avatar size (default: 'lg')

**Best For:** Modern, tech-focused interviews or when you need flexibility in size/style.

---

### 3. ProfessionalAvatar
**File:** `professional-avatar.tsx`

A clean, professional avatar design with minimalist aesthetics.

**Features:**
- Professional user icon design
- Customizable color schemes (blue, purple, green)
- AI badge indicator
- Smooth status transitions
- Audio level visualization bars
- Role/title display

**Usage:**
```tsx
import ProfessionalAvatar from '@/components/interview-session/professional-avatar';

<ProfessionalAvatar
  isSpeaking={aiSpeaking}
  name="Sarah Chen"
  role="Senior Technical Recruiter"
  avatarColor="blue"
/>
```

**Props:**
- `isSpeaking` (boolean, required): Whether the AI is currently speaking
- `name` (string, optional): Display name (default: "AI Interviewer")
- `role` (string, optional): Role/title (default: "Technical Recruiter")
- `avatarColor` ('blue' | 'purple' | 'green', optional): Color scheme (default: 'blue')

**Best For:** Professional, corporate interview settings where a business-like appearance is important.

---

## Implementation in Interview Page

The avatar is currently integrated in `/app/interview/page.tsx`:

### For Behavioral/Mixed Interviews (No Coding Problem)
The avatar appears in the center of the screen when the call is active:

```tsx
{(isCallActive || isConnecting) && (
  <div className="mb-8">
    <AnimatedFaceAvatar
      isSpeaking={aiSpeaking}
      name="AI Interviewer"
    />
  </div>
)}
```

### For Technical Interviews (With Coding Problem)
A mini avatar indicator appears in the header:

```tsx
{isTechnicalInterview && dsaProblem && isCallActive && (
  <div className="flex items-center gap-2">
    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500">
      <Volume2 className="w-5 h-5 text-white" />
    </div>
  </div>
)}
```

## Switching Avatar Components

To use a different avatar component:

1. Import the desired avatar component at the top of `interview/page.tsx`:
```tsx
// Change this:
import AnimatedFaceAvatar from '@/components/interview-session/animated-face-avatar';

// To this (for example):
import ProfessionalAvatar from '@/components/interview-session/professional-avatar';
```

2. Replace the component usage in the JSX:
```tsx
// Change this:
<AnimatedFaceAvatar isSpeaking={aiSpeaking} name="AI Interviewer" />

// To this:
<ProfessionalAvatar
  isSpeaking={aiSpeaking}
  name="AI Interviewer"
  role="Technical Interviewer"
  avatarColor="purple"
/>
```

## Customization Tips

### Adding New Animations
All three components use React `useEffect` hooks with `requestAnimationFrame` for smooth animations. To add new animations:

1. Create state for the animation value
2. Use `useEffect` with `isSpeaking` dependency
3. Use `requestAnimationFrame` for 60fps animations
4. Clean up with `cancelAnimationFrame` on unmount

### Color Customization
Each component uses Tailwind CSS classes. Modify the gradient colors:

```tsx
// AnimatedFaceAvatar
className="bg-gradient-to-br from-blue-100 via-purple-50 to-pink-100"

// TalkingAvatar
className="bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500"

// ProfessionalAvatar
const colors = {
  gradient: 'from-blue-600 to-blue-400',
  // ...other colors
}
```

### Size Adjustments
Modify the container dimensions:

```tsx
// Small avatar
className="w-24 h-24"

// Medium avatar
className="w-32 h-32"

// Large avatar (default)
className="w-48 h-48"
```

## Performance Considerations

- All animations use CSS transforms and `requestAnimationFrame` for optimal performance
- Components only animate when `isSpeaking={true}`
- Animations are automatically cleaned up on component unmount
- No external dependencies required - pure React and Tailwind CSS

## Browser Compatibility

All avatar components work on:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Accessibility

Current implementations include:
- Semantic HTML structure
- Color contrast ratios meeting WCAG AA standards
- Visual indicators for speaking/listening states

To improve accessibility:
- Add ARIA labels: `aria-label="AI Interviewer is speaking"`
- Add live region announcements: `<div aria-live="polite">{status}</div>`
- Consider reduced motion preferences: `prefers-reduced-motion` media query

## Future Enhancements

Potential improvements:
1. **Video Avatar Integration**: Use D-ID, Synthesia, or similar APIs for photorealistic video avatars
2. **Lip Sync**: More accurate mouth movements based on actual audio analysis
3. **Facial Expressions**: Add emotions (smile, thinking, nodding)
4. **Custom Avatars**: Allow users to upload their own interviewer image
5. **3D Avatars**: Integrate Three.js for 3D animated avatars
6. **Audio Analysis**: Use Web Audio API to visualize actual microphone input

## Example: Adding D-ID Video Avatar

To integrate a real video avatar service like D-ID:

```tsx
'use client';

import { useEffect, useRef } from 'react';

export default function VideoAvatar({ isSpeaking }: { isSpeaking: boolean }) {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    // Initialize D-ID or similar service
    // Stream video when isSpeaking changes
  }, [isSpeaking]);

  return (
    <div className="relative w-64 h-64 rounded-full overflow-hidden">
      <video
        ref={videoRef}
        className="w-full h-full object-cover"
        autoPlay
        playsInline
      />
    </div>
  );
}
```

This would require:
1. API key from D-ID/Synthesia
2. Installing their SDK: `npm install @d-id/client-sdk`
3. Streaming configuration
4. Additional backend support for video generation

## Support

For questions or issues with the avatar components, check:
- Component source code with inline comments
- Main interview page integration at `/app/interview/page.tsx`
- VAPI integration at `/lib/vapi/vapi-interviewer.ts`
