import type { AnalysisResponse } from "@/lib/api/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function analyzeRepository(
  url: string,
): Promise<AnalysisResponse> {
  if (!API_URL) {
    throw new Error("NEXT_PUBLIC_API_URL is not configured.");
  }

  let response: Response;

  try {
    response = await fetch(`${API_URL.replace(/\/$/, "")}/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }),
    });
  } catch {
    throw new Error("Unable to reach the RepoIntel API.");
  }

  if (!response.ok) {
    const payload: unknown = await response.json().catch(() => null);

    if (
      typeof payload === "object" &&
      payload !== null &&
      "detail" in payload &&
      typeof payload.detail === "string"
    ) {
      throw new Error(payload.detail);
    }

    throw new Error(
      `Repository analysis failed with HTTP status ${response.status}.`,
    );
  }

  try {
    return (await response.json()) as AnalysisResponse;
  } catch {
    throw new Error("The RepoIntel API returned an invalid JSON response.");
  }
}
