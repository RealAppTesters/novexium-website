export default async function handler(req, res) {
  // Enable CORS for form submissions
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }
  
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const FORMSPREE_ID = process.env.FORMSPREE_ID;
  
  if (!FORMSPREE_ID) {
    console.error('FORMSPREE_ID environment variable is not set');
    return res.status(500).json({ error: 'Form configuration error' });
  }

  try {
    // Forward the form data to Formspree
    const response = await fetch(`https://formspree.io/f/${FORMSPREE_ID}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(req.body)
    });
    
    const data = await response.json();
    
    if (response.ok) {
      return res.status(200).json({ success: true, data });
    } else {
      return res.status(response.status).json({ error: data });
    }
  } catch (error) {
    console.error('Form submission error:', error);
    return res.status(500).json({ error: 'Submission failed. Please try again.' });
  }
}
