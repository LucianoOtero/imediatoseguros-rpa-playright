    // Processar dados do lead - SUPORTE PARA AMBOS OS FORMATOS (como produção)
    // Formato 1: campos diretos (Webflow) $data["name"], $data["email"]
    // Formato 2: campos aninhados em data (Modal/RPA) $data["data"]["NOME"], $data["data"]["Email"]
    $name = isset($data["name"]) ? $data["name"] : (isset($data["nome"]) ? $data["nome"] : (isset($data["data"]["NOME"]) ? $data["data"]["NOME"] : "Nome não informado"));
    $email = isset($data["email"]) ? $data["email"] : (isset($data["data"]["Email"]) ? $data["data"]["Email"] : "");
    $phone = isset($data["phone"]) ? $data["phone"] : (isset($data["telefone"]) ? $data["telefone"] : (isset($data["data"]["DDD-CELULAR"]) && isset($data["data"]["CELULAR"]) ? $data["data"]["DDD-CELULAR"] . $data["data"]["CELULAR"] : ""));
    $gclid = isset($data["gclid"]) ? $data["gclid"] : (isset($data["data"]["GCLID_FLD"]) ? $data["data"]["GCLID_FLD"] : "");
    
    logDevWebhook("data_extracted", [
        "name" => $name,
        "email" => $email ? "present" : "missing",
        "phone" => $phone ? "present" : "missing",
        "gclid" => $gclid ? "present" : "missing",
        "format" => isset($data["data"]) ? "nested_data" : "direct_fields"
    ], true);
    
    $lead_data = [
        'firstName' => $name,
        'lastName' => '',
        'emailAddress' => $email,
        'phoneNumber' => $phone,
        'source' => 'Webflow Dev', // ✅ CORRETO para Lead
        'description' => 'Lead enviado do ambiente de desenvolvimento'
    ];











