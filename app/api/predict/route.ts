import { NextRequest, NextResponse } from "next/server";
export const runtime = "nodejs";
export async function POST(request: NextRequest) {
  const service = process.env.TOXICITY_API_URL;
  if (!service) return NextResponse.json({ error: "The prediction service has not been configured yet. Please contact the faculty administrator." }, { status: 503 });
  try {
    const body = await request.json();
    const smiles = typeof body.smiles === "string" ? body.smiles.trim() : "";
    if (!smiles || smiles.length > 2000) return NextResponse.json({ error: "Enter a valid SMILES string (maximum 2,000 characters)." }, { status: 400 });
    const response = await fetch(service.replace(/\/$/, "") + "/predict", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ smiles }), cache: "no-store"
    });
    const data = await response.json();
    return NextResponse.json(response.ok ? data : { error: typeof data.detail === "string" ? data.detail : (data.error || "Prediction failed.") }, { status: response.status });
  } catch {
    return NextResponse.json({ error: "Could not connect to the AI prediction service. Please try again later." }, { status: 502 });
  }
}
