# UPDATE THESE OFFSETS WHEN CSGO UPDATES. I WILL NOT BE UPDATING OFFSETS.
dwLocalPlayer = (0xD8B2BC)
m_hActiveWeapon = (0x2EF8)
dwForceJump = (0x524CEA4)
m_iHealth = (0x100)
m_vecVelocity = (0x114)
dwGlowObjectManager = (0x52EB540)
m_iGlowIndex = (0xA438)
m_flFlashMaxAlpha = (0xA41C)
m_fFlags = (0x104)
m_iObserverMode = (0x3378)
dwForceAttack = (0x31D44D4)
m_iTeamNum = (0xF4)
m_clrRender = (0x70)
dwEntityList = (0x4DA2F44)
m_iCrosshairId = (0xB3E4)
dwSetClanTag = (0x8A1A0)
m_bSpotted = (0x93D)
terrorist_color = [255, 50, 0]
triggerbot_enabled = 0
m_iHealth = (0x100)
def csgo_cheat():
	lol = 0
	print(Fore.CYAN + "[SyntheticAIO]: CSGO Python Hack by Luxiferr. With Love from Micro." + Fore.RESET)
	mem = pymem.Pymem("csgo.exe")
	moduleBase = pymem.process.module_from_name(mem.process_handle, "client.dll").lpBaseOfDll
	while True:
		try:
			player = mem.read_int(moduleBase + dwLocalPlayer)
		except:
			print("You're not in a game.")
		health = mem.read_int(player + m_iHealth)
		with open("Data\\cheat.json") as c:
			config = json.load(c)
		triggerbot_enabled = config.get('triggerbot')
		bhop_enabled = config.get('bhop')
		glow_enabled = config.get('glow')
		chams_enabled = config.get('chams')
		noflash_enabled = config.get('noflash')
		if player:
			if health > 0:
				on_ground = mem.read_int(player + m_fFlags)
				force_jump = moduleBase + dwForceJump
				glowMan = mem.read_int(moduleBase + dwGlowObjectManager)
				flash_value = player + m_flFlashMaxAlpha
				health = mem.read_int(player + m_iHealth)
				crosshairID = mem.read_int(player + m_iCrosshairId)
				getTeam = mem.read_int(moduleBase + dwEntityList + (crosshairID - 1) * 0x10)
				localTeam = mem.read_int(player + m_iTeamNum)
				crosshairTeam = mem.read_int(getTeam + m_iTeamNum)
				if crosshairID > 0 and crosshairID < 32 and localTeam != crosshairTeam and triggerbot_enabled == "enabled":
					mem.write_int(moduleBase + dwForceAttack, 6)
				if flash_value and noflash_enabled == "enabled":
					mem.write_float(flash_value, float(0))
				if keyboard.is_pressed('space') and bhop_enabled == "enabled":
					if on_ground and on_ground == 257:
						mem.write_int(force_jump, 5)
						time.sleep(0.05)
						mem.write_int(force_jump, 4)
				if keyboard.is_pressed('v') and lol == 0:
					mem.write_int(player + m_iObserverMode, 1)
					lol = 1
					print("Thirdperson Enabled!")
					time.sleep(0.6)
				if keyboard.is_pressed('v') and lol == 1:
					mem.write_int(player + m_iObserverMode, 0)
					lol = 0
					print("Thirdperson Disabled!")
					time.sleep(0.6)
				if glow_enabled == "enabled":
					for x in range(1,32):
						entity = mem.read_int(moduleBase + dwEntityList + x * 0x10)	
						if entity:
							entity_id = mem.read_int(entity + m_iTeamNum)
							entityGlow = mem.read_int(entity + m_iGlowIndex)
							if entity_id != localTeam:
								mem.write_float(glowMan + entityGlow * 0x38 + 0x4, float(1))
								mem.write_float(glowMan + entityGlow * 0x38 + 0x8, float(0))
								mem.write_float(glowMan + entityGlow * 0x38 + 0xC, float(0))
								mem.write_float(glowMan + entityGlow * 0x38 + 0x10, float(1))
								mem.write_int(glowMan + entityGlow * 0x38 + 0x24, 1)
								#radar
								mem.write_int(entity + m_bSpotted, 1)
								#chams
								mem.write_int(entity + m_clrRender, (terrorist_color[0]))
								mem.write_int(entity + m_clrRender + 0x1, (terrorist_color[1]))
								mem.write_int(entity + m_clrRender + 0x2, (terrorist_color[2]))
			else:
				print("Player is dead. Waiting.")
				time.sleep(2)

		else:
			print("Not Ingame.")
			time.sleep(2)

csgo_cheat()