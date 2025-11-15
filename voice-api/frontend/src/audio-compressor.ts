/**
 * Audio Compression Utilities
 * Compress audio files before sending to reduce upload size
 */

export interface CompressionOptions {
  quality?: number; // 0.0 to 1.0
  bitrate?: number; // bits per second
  maxSizeBytes?: number; // Maximum target size
}

/**
 * Compress audio blob using Web Audio API
 * Note: This is a client-side compression approximation
 * For true compression, use server-side processing
 */
export async function compressAudioBlob(
  blob: Blob,
  options: CompressionOptions = {}
): Promise<Blob> {
  const { maxSizeBytes } = options;

  // If blob is already small enough, return as-is
  if (maxSizeBytes && blob.size <= maxSizeBytes) {
    return blob;
  }

  try {
    // Calculate compression ratio if maxSizeBytes is specified
    if (maxSizeBytes) {
      const currentSize = blob.size;
      const ratio = maxSizeBytes / currentSize;
      if (ratio < 1.0) {
        console.warn(`File size (${(currentSize / 1024 / 1024).toFixed(2)}MB) exceeds target. Consider server-side compression.`);
      }
    }

    // For now, return original blob
    // True compression would require server-side processing
    // or using a library like lamejs for MP3 encoding
    // Client-side compression is limited - use server-side compression for best results
    console.warn('Client-side audio compression is limited. Consider server-side compression.');
    
    return blob;
  } catch (error) {
    console.error('Compression failed, returning original:', error);
    return blob;
  }
}

/**
 * Check if audio needs compression
 */
export function needsCompression(blob: Blob, maxSizeBytes: number = 25 * 1024 * 1024): boolean {
  return blob.size > maxSizeBytes;
}

/**
 * Get compression recommendation
 */
export function getCompressionRecommendation(blob: Blob): {
  needsCompression: boolean;
  currentSizeMB: number;
  recommendedAction: string;
} {
  const maxSizeMB = 25;
  const currentSizeMB = blob.size / (1024 * 1024);
  const needsCompression = currentSizeMB > maxSizeMB;

  let recommendedAction = 'No compression needed';
  if (needsCompression) {
    recommendedAction = `File is ${currentSizeMB.toFixed(2)}MB. Consider server-side compression or reducing recording duration.`;
  }

  return {
    needsCompression,
    currentSizeMB,
    recommendedAction
  };
}

