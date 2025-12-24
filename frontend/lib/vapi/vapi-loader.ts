/**
 * Vapi SDK Loader
 * Handles loading Vapi Web SDK for browser use
 */

// Import Vapi - handle both default and named exports
import VapiSDK from '@vapi-ai/web';

// The package exports as default (CommonJS), Vite will handle the conversion
// @ts-ignore - VapiSDK might have a default property at runtime
export const Vapi = (VapiSDK as any).default || VapiSDK;
export default Vapi;

