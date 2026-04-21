export async function getEnv() {
    try {
        const response = await fetch('../.env');
        const text = await response.text();
        const env = {};
        
        text.split('\n').forEach(line => {
            const [key, ...value] = line.split('=');
            if (key && value.length > 0) {
                env[key.trim()] = value.join('=').trim();
            }
        });

        return {
            firebaseConfig: {
                apiKey: env.FIREBASE_API_KEY,
                authDomain: env.FIREBASE_AUTH_DOMAIN,
                projectId: env.FIREBASE_PROJECT_ID,
                storageBucket: env.FIREBASE_STORAGE_BUCKET,
                messagingSenderId: env.FIREBASE_MESSAGING_SENDER_ID,
                appId: env.FIREBASE_APP_ID,
                measurementId: env.FIREBASE_MEASUREMENT_ID
            },
            aiApiKey: env.AI_API_KEY
        };
    } catch (e) {
        console.error("Failed to load .env file", e);
        return { firebaseConfig: {}, aiApiKey: "" };
    }
}
