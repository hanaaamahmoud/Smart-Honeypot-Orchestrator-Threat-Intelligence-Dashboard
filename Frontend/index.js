async function getFollowers() {
    try {
        const response = await


            // دا الجزء اللي بيتغير بس 

            fetch("https://www.instagram.com/api/v1/friendships/41921836037/followers/?count=12&search_surface=follow_list_page", {
                "headers": {
                    "accept": "*/*",
                    "accept-language": "en-US,en;q=0.9",
                    "priority": "u=1, i",
                    "sec-ch-prefers-color-scheme": "dark",
                    "sec-ch-ua": "\"Chromium\";v=\"152\", \"Not?A_Brand\";v=\"24\", \"Google Chrome\";v=\"152\"",
                    "sec-ch-ua-full-version-list": "\"Chromium\";v=\"152.0.7977.64\", \"Not?A_Brand\";v=\"24.0.0.0\", \"Google Chrome\";v=\"152.0.7977.64\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-model": "\"\"",
                    "sec-ch-ua-platform": "\"Linux\"",
                    "sec-ch-ua-platform-version": "\"\"",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "x-asbd-id": "359341",
                    "x-csrftoken": "L69z0cHE2FE8QFPnDG4fQVtwt3KS0T5B",
                    "x-ig-app-id": "936619743392459",
                    "x-ig-max-touch-points": "10",
                    "x-ig-www-claim": "hmac.AR1eTX-CUGg4TW-WsD4uPzOmmC-c-KI4shOA0DH_Mr5uiRHC",
                    "x-requested-with": "XMLHttpRequest",
                    "x-web-session-id": "7igu5h:dmvhjx:fkp53w",
                    "cookie": "ig_did=A8AF897B-AAF0-4342-8AC0-E673E707A75C; datr=dZWoalzJVJ-ld3xcyI-Ocrje; mid=aqiVdQAEAAHUu9IWCHGBaHn2KYLP; rd_challenge=Q_6hBQTkzmIkdJGOte1OFm7YXJJMXgWaw_FpIgpqMIHbdp5j8IJZSc9wPkTXBDLDplNiib2O4muY2se5XxY_sa57h2hd; csrftoken=L69z0cHE2FE8QFPnDG4fQVtwt3KS0T5B; ds_user_id=12306863300; sessionid=12306863300%3ARB05jHx68s4C1Z%3A21%3AAYmjR64J0YxXij8UfXmhjoGMmFicdncJo_369fBilA; wd=850x769; rur=CLN%2C17841412459008357%2C1790645896%3A01ff50ee23f38151d39879d841ae4fac845ba885b6c1e289c20df58c1abc82acd4f9058b",
                    "Referer": "https://www.instagram.com/maryam_eh137/"
                },
                "body": null,
                "method": "GET"
            });

        if (!response.ok) {
            throw new Error(
                `HTTP Error: ${response.status} ${response.statusText}`
            );
        }

        const data = await response.json();
        return data.users;

    } catch (error) {
        console.error("Error fetching followers:", error);
        return null;
    }
}


const users = await getFollowers();
console.log(users)



async function createGroupThread() {
    try {
        const recipient_users = ["38749656467"];
        const encoded = encodeURIComponent(
            JSON.stringify(recipient_users)
        );

        const response = await


            // دا الجزء اللي بيتغير بس 

            fetch("https://www.instagram.com/api/v1/direct_v2/create_group_thread/", {
                "headers": {
                    "accept": "*/*",
                    "accept-language": "en-US,en;q=0.9",
                    "content-type": "application/x-www-form-urlencoded",
                    "priority": "u=1, i",
                    "sec-ch-prefers-color-scheme": "dark",
                    "sec-ch-ua": "\"Chromium\";v=\"152\", \"Not?A_Brand\";v=\"24\", \"Google Chrome\";v=\"152\"",
                    "sec-ch-ua-full-version-list": "\"Chromium\";v=\"152.0.7977.64\", \"Not?A_Brand\";v=\"24.0.0.0\", \"Google Chrome\";v=\"152.0.7977.64\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-model": "\"\"",
                    "sec-ch-ua-platform": "\"Linux\"",
                    "sec-ch-ua-platform-version": "\"\"",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "x-asbd-id": "359341",
                    "x-csrftoken": "L69z0cHE2FE8QFPnDG4fQVtwt3KS0T5B",
                    "x-ig-app-id": "936619743392459",
                    "x-ig-max-touch-points": "10",
                    "x-ig-www-claim": "hmac.AR1eTX-CUGg4TW-WsD4uPzOmmC-c-KI4shOA0DH_Mr5uiRHC",
                    "x-instagram-ajax": "1047523314",
                    "x-requested-with": "XMLHttpRequest",
                    "x-web-session-id": "sm44d4:dmvhjx:2tzptx",
                    "cookie": "ig_did=A8AF897B-AAF0-4342-8AC0-E673E707A75C; datr=dZWoalzJVJ-ld3xcyI-Ocrje; mid=aqiVdQAEAAHUu9IWCHGBaHn2KYLP; rd_challenge=Q_6hBQTkzmIkdJGOte1OFm7YXJJMXgWaw_FpIgpqMIHbdp5j8IJZSc9wPkTXBDLDplNiib2O4muY2se5XxY_sa57h2hd; csrftoken=L69z0cHE2FE8QFPnDG4fQVtwt3KS0T5B; ds_user_id=12306863300; sessionid=12306863300%3ARB05jHx68s4C1Z%3A21%3AAYmjR64J0YxXij8UfXmhjoGMmFicdncJo_369fBilA; wd=850x769; rur=CLN%2C17841412459008357%2C1790647596%3A01ff644f744157972f9b16e389f66727b805c9bd98128fffbee77d5ee8a0fdd3c01f107c",
                    "Referer": "https://www.instagram.com/maryam_eh137/"
                },
                "body": `recipient_users=${encoded}&fb_dtsg=NAfz7iSL2L2531DGO821y5p44T1grkYjjq9OMOuldeqhG7PANxP1e2g%3A17843696212148243%3A1789433655&jazoest=22454`,
                "method": "POST"
            });

        if (!response.ok) {
            throw new Error(
                `HTTP Error: ${response.status} ${response.statusText}`
            );
        }

        const data = await response.json();

        console.log("Group thread created:", data.messaging_thread_key);
        return data.thread_v2_id;

    } catch (error) {
        console.error("Error creating group thread:", error);
        return null;
    }
}

const thread_fbid = await createGroupThread();





async function getChatThread(thread_fbid) {
    try {
        const variables =
            `variables=${encodeURIComponent(
                JSON.stringify({
                    min_uq_seq_id: "14295",
                    thread_fbid: thread_fbid,
                    __relay_internal__pv__IGDEnableOffMsysChatThemesQErelayprovider: false,
                    __relay_internal__pv__IGDInitialMessagePageCountrelayprovider: 20
                })
            )}&doc_id=26031375673226515`;

        const response = await



            fetch("https://www.instagram.com/api/graphql", {
                "headers": {
                    "accept": "*/*",
                    "accept-language": "en-US,en;q=0.9",
                    "content-type": "application/x-www-form-urlencoded",
                    "priority": "u=1, i",
                    "sec-ch-prefers-color-scheme": "dark",
                    "sec-ch-ua": "\"Chromium\";v=\"152\", \"Not?A_Brand\";v=\"24\", \"Google Chrome\";v=\"152\"",
                    "sec-ch-ua-full-version-list": "\"Chromium\";v=\"152.0.7977.64\", \"Not?A_Brand\";v=\"24.0.0.0\", \"Google Chrome\";v=\"152.0.7977.64\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-model": "\"\"",
                    "sec-ch-ua-platform": "\"Linux\"",
                    "sec-ch-ua-platform-version": "\"\"",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "x-asbd-id": "359341",
                    "x-csrftoken": "L69z0cHE2FE8QFPnDG4fQVtwt3KS0T5B",
                    "x-fb-friendly-name": "IGDChatTabRootOffMsysQuery",
                    "x-fb-lsd": "rVUOnU3LKRQZ8ikwm_57y1",
                    "x-ig-app-id": "936619743392459",
                    "x-ig-max-touch-points": "10",
                    "cookie": "ig_did=A8AF897B-AAF0-4342-8AC0-E673E707A75C; datr=dZWoalzJVJ-ld3xcyI-Ocrje; mid=aqiVdQAEAAHUu9IWCHGBaHn2KYLP; rd_challenge=Q_6hBQTkzmIkdJGOte1OFm7YXJJMXgWaw_FpIgpqMIHbdp5j8IJZSc9wPkTXBDLDplNiib2O4muY2se5XxY_sa57h2hd; csrftoken=L69z0cHE2FE8QFPnDG4fQVtwt3KS0T5B; ds_user_id=12306863300; wd=850x769; sessionid=12306863300%3ARB05jHx68s4C1Z%3A21%3AAYkxD0xP6qKb8Tl0clTe9e4haAHHsmeGedHg6N62uQ; rur=CLN%2C17841412459008357%2C1790651429%3A01ffd6a9eb9f0f5b1c45aa40a2c07bfa85b9448b4be51ebcd9d213abfb91d9b5bc8a7ad3",
                    "Referer": "https://www.instagram.com/maryam_eh137/"
                },
                "body": `av=17841412459008357
            &__d=www
            &__user=0
            &__a=1
            &__req=13
            &__hs=20711.HYP%3Ainstagram_web_pkg.2.1...0
            &dpr=1
            &__ccg=POOR&__rev=1047523314
            &__s=t0ptef%3Admvhjx%3Asj2l5z
            &__hsi=7685594039789145168
            &__dyn=7xeUjG1mxu1syaxG4Vp41twpUnwgU7SbzEdF8vyUco2qwJyEiw50x609vCwjE1EEc87m0yE462mcw5Mx62G5UswoEcE7O2l0Fwqo5W1yw9O1lwxwQzXwae4UaEW2G0AEco5G0zK5o4q0HU1wEbUGdwtUeo9UaQ0Lo6-bwHwKG6Ufk0zU8oC1IwjUpwlAcwBwUQp1yU426V8aUuwm8jxK1mwa6bBK4o16UeUGq2Kq11whE984O0XEdoCQ1jwfetch("https://www.instagram.com/api/graphql", {
  "headers": {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded",
    "priority": "u=1, i",
    "sec-ch-prefers-color-scheme": "dark",
    "sec-ch-ua": "\"Chromium\";v=\"152\", \"Not?A_Brand\";v=\"24\", \"Google Chrome\";v=\"152\"",
    "sec-ch-ua-full-version-list": "\"Chromium\";v=\"152.0.7977.64\", \"Not?A_Brand\";v=\"24.0.0.0\", \"Google Chrome\";v=\"152.0.7977.64\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-ch-ua-platform-version": "\"\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-asbd-id": "359341",
    "x-csrftoken": "L69z0cHE2FE8QFPnDG4fQVtwt3KS0T5B",
    "x-fb-friendly-name": "IGDChatTabRootOffMsysQuery",
    "x-fb-lsd": "rVUOnU3LKRQZ8ikwm_57y1",
    "x-ig-app-id": "936619743392459",
    "x-ig-max-touch-points": "10",
    "cookie": "ig_did=A8AF897B-AAF0-4342-8AC0-E673E707A75C; datr=dZWoalzJVJ-ld3xcyI-Ocrje; mid=aqiVdQAEAAHUu9IWCHGBaHn2KYLP; rd_challenge=Q_6hBQTkzmIkdJGOte1OFm7YXJJMXgWaw_FpIgpqMIHbdp5j8IJZSc9wPkTXBDLDplNiib2O4muY2se5XxY_sa57h2hd; csrftoken=L69z0cHE2FE8QFPnDG4fQVtwt3KS0T5B; ds_user_id=12306863300; wd=850x769; sessionid=12306863300%3ARB05jHx68s4C1Z%3A21%3AAYkxD0xP6qKb8Tl0clTe9e4haAHHsmeGedHg6N62uQ; rur=CLN%2C17841412459008357%2C1790651429%3A01ffd6a9eb9f0f5b1c45aa40a2c07bfa85b9448b4be51ebcd9d213abfb91d9b5bc8a7ad3",
    "Referer": "https://www.instagram.com/maryam_eh137/"
  },
  "body": "av=17841412459008357&__d=www&__user=0&__a=1&__req=13&__hs=20711.HYP%3Ainstagram_web_pkg.2.1...0&dpr=1&__ccg=POOR&__rev=1047523314&__s=t0ptef%3Admvhjx%3Asj2l5z&__hsi=7685594039789145168&__dyn=7xeUjG1mxu1syaxG4Vp41twpUnwgU7SbzEdF8vyUco2qwJyEiw50x609vCwjE1EEc87m0yE462mcw5Mx62G5UswoEcE7O2l0Fwqo5W1yw9O1lwxwQzXwae4UaEW2G0AEco5G0zK5o4q0HU1wEbUGdwtUeo9UaQ0Lo6-bwHwKG6Ufk0zU8oC1IwjUpwlAcwBwUQp1yU426V8aUuwm8jxK1mwa6bBK4o16UeUGq2Kq11whE984O0XEdoCQ1jw&__csr=hIA4A514zitqPifqbn8DN7O5bEH5ip4BGWpRV9djADq-H98umqVaGKzSxqaJbqilKBLJkye_UWiZAi9l5jKBLjp94nFiIBBbQkGplptTuJj9aBFrqlt4yllDBjny9tanBAGa8HroSiKimAQ9AKaAyGBg_AxmiVEGUKiiq8xW4KVEWh2EZ3EZ1eUhDoy2e4J4zXuuaBhO2oWu6k9oW8zUjBz8Gmiiu5V8V1a6FtwAKVF4uaxqFUowc-0YU2Uw40DUc8hAw0a-600N9E9U5i0bDw6pwLB9gy2W4m04XE1MINS0mdwkQ5o0vZS0Kod8b8N0OwzwwwNw7Vxsne0gu0me0mm6838Fxi2y16y4m0_oOaApdo0VWU0xNw0ov80uBw0zXw0E8w&__hsdp=g4fd9E6kqLgULqhar4hBa8tbcFnp2m57AiUn1bzlnc8PQWGfj98p0Gxa3bwBgF8E7m2K441lwh9dAhe8xe4HAyEekgzwUwTxC2eq1DwKG1Twmu14DCwi458G3u484m1Gxm0zU9UpwEyosK1Uwwxy7UuwHwiU3hU0wS3C0b3w3dU119U7i07e86q1awl9lwEwpF80Km2u0hR0r81E84C0N80gBw4CwtE5q0XAUgxjwXw9irw&__hblp=0Dx_wmEeEb8a8rgqGmCax6223y48jwwx3wAp8GfzEjCJ1W3KbxybwBwNxe584iiurQm4UgXjUymdVoaEy2-6Ki5opyopCwUUb8jxGEco45aqbx63jwVyFVE4x1iawTzQ2DxC7U4Gi482bK2u49CdxG9xOU7y224HUvxWu6VV84q1IAyU5fw5Oxa0xUeo30wfi2S0x89od84C781Fo1aE119U7i0fUw7hw9q0xE4-14wxwZz8-14Bm2x0HgcUqwRw2DE9U30wn4dwgK6ogw6fwio7e1gw37Q0Do4idxe0RoW11Axy1owDwKw9m1ojx25e3K8w8Krw&__sjsp=g4fayq2c44qLzOy4iCN4piy7iPalSgBxhVqxA4K2S6A0K4E0Ga&__comet_req=7&fb_dtsg=NAfyv8N-inYCOmZLWa0zVi39gZMlrkbdEiA2XZTegT26QwpjQ4K-X_A%3A17843696212148243%3A1789433655&jazoest=26234&lsd=rVUOnU3LKRQZ8ikwm_57y1&__spin_r=1047523314&__spin_b=trunk&__spin_t=1789441807&__crn=comet.igweb.PolarisProfilePostsTabRoute&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=IGDChatTabRootOffMsysQuery&server_timestamps=true
  &variables=${variables}",
  "method": "POST"
});&__csr=hIA4A514zitqPifqbn8DN7O5bEH5ip4BGWpRV9djADq-H98umqVaGKzSxqaJbqilKBLJkye_UWiZAi9l5jKBLjp94nFiIBBbQkGplptTuJj9aBFrqlt4yllDBjny9tanBAGa8HroSiKimAQ9AKaAyGBg_AxmiVEGUKiiq8xW4KVEWh2EZ3EZ1eUhDoy2e4J4zXuuaBhO2oWu6k9oW8zUjBz8Gmiiu5V8V1a6FtwAKVF4uaxqFUowc-0YU2Uw40DUc8hAw0a-600N9E9U5i0bDw6pwLB9gy2W4m04XE1MINS0mdwkQ5o0vZS0Kod8b8N0OwzwwwNw7Vxsne0gu0me0mm6838Fxi2y16y4m0_oOaApdo0VWU0xNw0ov80uBw0zXw0E8w&__hsdp=g4fd9E6kqLgULqhar4hBa8tbcFnp2m57AiUn1bzlnc8PQWGfj98p0Gxa3bwBgF8E7m2K441lwh9dAhe8xe4HAyEekgzwUwTxC2eq1DwKG1Twmu14DCwi458G3u484m1Gxm0zU9UpwEyosK1Uwwxy7UuwHwiU3hU0wS3C0b3w3dU119U7i07e86q1awl9lwEwpF80Km2u0hR0r81E84C0N80gBw4CwtE5q0XAUgxjwXw9irw&__hblp=0Dx_wmEeEb8a8rgqGmCax6223y48jwwx3wAp8GfzEjCJ1W3KbxybwBwNxe584iiurQm4UgXjUymdVoaEy2-6Ki5opyopCwUUb8jxGEco45aqbx63jwVyFVE4x1iawTzQ2DxC7U4Gi482bK2u49CdxG9xOU7y224HUvxWu6VV84q1IAyU5fw5Oxa0xUeo30wfi2S0x89od84C781Fo1aE119U7i0fUw7hw9q0xE4-14wxwZz8-14Bm2x0HgcUqwRw2DE9U30wn4dwgK6ogw6fwio7e1gw37Q0Do4idxe0RoW11Axy1owDwKw9m1ojx25e3K8w8Krw&__sjsp=g4fayq2c44qLzOy4iCN4piy7iPalSgBxhVqxA4K2S6A0K4E0Ga&__comet_req=7&fb_dtsg=NAfyv8N-inYCOmZLWa0zVi39gZMlrkbdEiA2XZTegT26QwpjQ4K-X_A%3A17843696212148243%3A1789433655&jazoest=26234&lsd=rVUOnU3LKRQZ8ikwm_57y1&__spin_r=1047523314&__spin_b=trunk&__spin_t=1789441807&__crn=comet.igweb.PolarisProfilePostsTabRoute&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=IGDChatTabRootOffMsysQuery&server_timestamps=true&variables=%7B%22min_uq_seq_id%22%3A%2214295%22%2C%22thread_fbid%22%3A%2218078273071396038%22%2C%22__relay_internal__pv__IGDEnableOffMsysChatThemesQErelayprovider%22%3Afalse%2C%22__relay_internal__pv__IGDInitialMessagePageCountrelayprovider%22%3A20%7D&doc_id=26031375673226515`,
                "method": "POST"
            });
        if (!response.ok) {
            throw new Error(
                `HTTP Error: ${response.status} ${response.statusText}`
            );
        }

        const raw = await response.text();

        const clean = raw
            .replace(/^for\s*\(\s*;;\s*\);/, "")
            .trim();

        const data = JSON.parse(clean);

        console.log("Chat thread:", data.data.get_slide_thread_nullable.as_ig_direct_thread.thread_id);

        return data;

    } catch (error) {
        console.error("Error fetching chat thread:", error);
        return null;
    }
}


// غيّر الـ thread فقط هنا
getChatThread("18084882209288468");








































async function sendRequest() {
    const variables = encodeURIComponent(
        JSON.stringify({
            ig_thread_igid: "2003064050557860",
            offline_threading_id: "7505468124359424780",
            recipient_igids: null,
            replied_to_client_context: null,
            replied_to_item_id: null,
            reply_to_message_id: null,
            sampled: null,
            text: {
                sensitive_string_value: "انا مش انسان"
            },
            mentions: [],
            mentioned_user_ids: [],
            commands: null,
            forwarded_from_thread_id: null,
            is_forwarded_from_own_message: null,
            send_attribution: "igd_web_chat_tab:in_thread"
        })
    )



    try {
        const response = await

            //

fetch("https://www.instagram.com/api/graphql", {
  "headers": {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded",
    "priority": "u=1, i",
    "sec-ch-prefers-color-scheme": "dark",
    "sec-ch-ua": "\"Chromium\";v=\"152\", \"Not?A_Brand\";v=\"24\", \"Google Chrome\";v=\"152\"",
    "sec-ch-ua-full-version-list": "\"Chromium\";v=\"152.0.7977.64\", \"Not?A_Brand\";v=\"24.0.0.0\", \"Google Chrome\";v=\"152.0.7977.64\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-ch-ua-platform-version": "\"\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-asbd-id": "359341",
    "x-csrftoken": "L69z0cHE2FE8QFPnDG4fQVtwt3KS0T5B",
    "x-fb-friendly-name": "IGDirectTextSendMutation",
    "x-fb-lsd": "C5q6CVpyZfnr_jAoA1XyPb",
    "x-ig-app-id": "936619743392459",
    "x-ig-max-touch-points": "10",
    "cookie": "ig_did=A8AF897B-AAF0-4342-8AC0-E673E707A75C; datr=dZWoalzJVJ-ld3xcyI-Ocrje; mid=aqiVdQAEAAHUu9IWCHGBaHn2KYLP; rd_challenge=Q_6hBQTkzmIkdJGOte1OFm7YXJJMXgWaw_FpIgpqMIHbdp5j8IJZSc9wPkTXBDLDplNiib2O4muY2se5XxY_sa57h2hd; csrftoken=L69z0cHE2FE8QFPnDG4fQVtwt3KS0T5B; ds_user_id=12306863300; wd=850x769; sessionid=12306863300%3ARB05jHx68s4C1Z%3A21%3AAYkxD0xP6qKb8Tl0clTe9e4haAHHsmeGedHg6N62uQ; rur=CLN%2C17841412459008357%2C1790655442%3A01ff2327ddd9f973bae35bf3126d27c10021b3031b6d48424bece5a9c727ec9adc3f9551",
    "Referer": "https://www.instagram.com/maryam_eh137/"
  },
  "body": `av=17841412459008357&__d=www&__user=0&__a=1&__req=1c&__hs=20711.HYP%3Ainstagram_web_pkg.2.1...0&dpr=1&__ccg=POOR&__rev=1047530023&__s=isiyxo%3Admvhjx%3A3vkevz&__hsi=7685610786934164984&__dyn=7xeUjG1mxu1syaxG4Vp41twpUnwgU7SbzEdF8vyUco2qwJyEiw9-1DwUx609vCwjE1EEc87m0yE462mcw5Mx62G5UswoEcE7O2l0Fwqo5W1yw9O1lwxwQzXwae4UaEW2G0AEco5G0zK5o4q1qwl81wEbUGdwtUeo9UaQ0Lo6-bwHwKG6Ufk0zU8oC1IwjUpwlAcwBwUQp6x6U42UnAwHxW1oxe6U5q0EoKmUhw4rwXyFEaVE4616wAwj83KwRyrg5e&__csr=gB3QdMzP8IBaARcioYhd24ymzThb_9tlXl5WWKaCtii2r8UyLoNJvF8WbOikBmIy5eWDW9ijCnFHhvS_AnthlGqzROWQQKWFdOQjBFSBsBDOsDCEyox8wxfmjQi42KniQJbQnBQYxucJ6zazqyAjGi-mcBGQidyryUjGJ29qF6y9Xzp4GABx6WAy47p9efGQ8yFEydy8HmeKqDVt6BGcxucDy4HCgWdDyHKcGUGex6dBAz8BubglAghgm8q4uu8yFU2Gm0HE5G1pwbNw3yo02ygwdm00N9o9U5i0bCw6BwzAbwUx0w0jGw6YCtxe9gkw4Wo5bxm0P80sEDm0Ko6m8wzzXx-4oW1Sw6sG545Nsw11U8ngnw4Bw5Dxy0NGokx21uDVo3CwPpnAg0VKi08no067u07rUdo0jeg0gHw3-y3U0nWwdybw&__hsdp=g4gDq1J6LhoALqQlQxAiUxQPpBOdQmeCcUn1ae8Bc8kO_MBq98vcoxi3UiwRU95XhYM722u443S1zKSlaiahGgszEcP28e8eoW7o-1TwACw8Ou12wYyXwPzWzo4C7EC1GwLway6EuwKyUnwkpUZ0pUtwBwiUG3m0gy0zo0gaw3do10VU7i07dU6u19wkVJ0EwqQ0bywDw4ny86K0oC1vwca04eE1587m1jweZe48kUf82iCU&__hblp=1G2Om1qwXwDzodK5VGWiwzwFwBx6Egwwx2q7p4FouAxbKqWUnwKxi6K7oy3Cey85GUyqCahGp8K9hLJ1y2ui3emUy9DxiezFoycG3m5qzEjhaBxKq1sykfxiiGzE999EbucyXyEa4eQdwTx51GEC58y1cBxe5pE2tF4xm6HwEByUnwkpUZ3kmGwje6Uky9VbwgEG3m1xwaq0zo3dxy1mwVwGwZwi89o88eAm0NU2fwk8swAw5Mw4Nw43Dwt80_C1twbC1iwp822waa17wh88Eb8sx212CQ2x0IAwKxG3K0uW582iwDwbq1wy8O12Upxu0iWEfU5-1PwjE0O1o5i18wgu3i0Mo8ocbxC1nwAwKwjU5m19jx25e3O8wHwnpK&__sjsp=g4gACwz196LgYEzhni6hby7jdCn8TholOe5Mizy9j25cKZhZEAwAFO580wKQvAw5Yw4dw&__comet_req=7&fb_dtsg=NAfxRhyavUJAsGtvAZIEFOffYIccqgBMwg0Mc-ROx1vBj-JCbwhJ0wQ%3A17843696212148243%3A1789433655&jazoest=26374&lsd=C5q6CVpyZfnr_jAoA1XyPb&__spin_r=1047530023&__spin_b=trunk&__spin_t=1789445706&__crn=comet.igweb.PolarisProfilePostsTabRoute&qpl_active_flow_ids=25313175%2C354954279&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=IGDirectTextSendMutation&server_timestamps=true&variables=${variables}&doc_id=26911679871773184&fb_api_analytics_tags=%5B%22qpl_active_flow_ids%3D25313175%2C354954279%22%5D`,
  "method": "POST"
});
        if (!response.ok) {
            throw new Error(
                `HTTP Error: ${response.status} ${response.statusText}`
            );
        }

        const raw = await response.text();

        const clean = raw
            .replace(/^for\s*\(\s*;;\s*\);/, "")
            .trim();

        const data = JSON.parse(clean);

        console.log("Chat thread:", data);

        return data;

    } catch (error) {
        console.error("Error fetching chat thread:", error);
        return null;
    }
}

sendRequest()