import time
import tls_client

class StakePyError(Exception):
    pass

class Stake:
    def __init__(self, api_key: str, user_agent: str, cf_clearance: str) -> None:
        self.api_key = api_key
        self.user_agent = user_agent
        self.cf_clearance = cf_clearance

        self.session = tls_client.Session(
            client_identifier="chrome_108",
            random_tls_extension_order=True
        )

    def get_convert_rate(self) -> dict:
        if self.api_key == None:
            raise StakePyError("APIキーの指定が必要です")

        response = self.session.post(
            "https://stake.com/_api/graphql",
            headers={
                "Content-Type": "application/json",
                "User-Agent": self.user_agent,
                "X-Access-Token": self.api_key
            },
            json={
                "query": "query CurrencyConversionRate {\n  info {\n    currencies {\n      name\n      eur: value(fiatCurrency: eur)\n      jpy: value(fiatCurrency: jpy)\n      usd: value(fiatCurrency: usd)\n      brl: value(fiatCurrency: brl)\n      cad: value(fiatCurrency: cad)\n      cny: value(fiatCurrency: cny)\n      idr: value(fiatCurrency: idr)\n      inr: value(fiatCurrency: inr)\n      krw: value(fiatCurrency: krw)\n      php: value(fiatCurrency: php)\n      rub: value(fiatCurrency: rub)\n      mxn: value(fiatCurrency: mxn)\n      dkk: value(fiatCurrency: dkk)\n    }\n  }\n}\n",
                "variables": {}
            },
            cookies={
                "cf_clearance": self.cf_clearance
            }
        ).json()

        return response
    
    def get_notification(self, limit: int = 20) -> dict:
        if self.api_key == None:
            raise StakePyError("APIキーの指定が必要です")

        response = self.session.post(
            "https://stake.com/_api/graphql",
            headers={
                "Content-Type": "application/json",
                "User-Agent": self.user_agent,
                "X-Access-Token": self.api_key
            },
            json={
                "query": "query NotificationList($limit: Int, $offset: Int) {\n  user {\n    id\n    notificationList(limit: $limit, offset: $offset) {\n      ...Notification\n    }\n  }\n}\n\nfragment Notification on Notification {\n  id\n  type\n  acknowledged\n  __typename\n  data {\n    __typename\n    ... on NotificationKyc {\n      kycStatus: status\n    }\n    ... on UserFlag {\n      createdAt\n      flag\n    }\n    ... on ChatTip {\n      createdAt\n      currency\n      amount\n      sendBy {\n        name\n      }\n    }\n    ... on NotificationKycBanned {\n      kycBannedMessage: message\n    }\n    ... on ChatRainUser {\n      amount\n      currency\n      rain {\n        createdAt\n        sendBy {\n          name\n        }\n      }\n    }\n    ... on CashAdvance {\n      id\n      advanceAmount\n      currency\n      createdAt\n    }\n    ... on UserBonus {\n      createdAt\n      currency\n      amount\n      credit\n    }\n    ... on SportBet {\n      id\n      amount\n      active\n      currency\n      status\n      payoutMultiplier\n      cashoutMultiplier\n      payout\n      createdAt\n      system\n      potentialMultiplier\n      adjustments {\n        id\n        payoutMultiplier\n        updatedAt\n        createdAt\n      }\n      user {\n        id\n        name\n      }\n      search {\n        iid\n      }\n      outcomes {\n        odds\n        status\n        outcome {\n          id\n          name\n          active\n          odds\n        }\n        market {\n          ...SportMarket\n        }\n        fixture {\n          id\n          slug\n          provider\n          tournament {\n            ...TournamentTree\n          }\n          data {\n            ...SportFixtureDataMatch\n            ...SportFixtureDataOutright\n            __typename\n          }\n        }\n      }\n    }\n    ... on SwishBet {\n      ...SwishBetFragment\n    }\n    ... on WalletDeposit {\n      id\n      createdAt\n      amount\n      currency\n      chain\n      walletStatus: status\n      tokensReceived {\n        currency\n        amount\n      }\n    }\n    ... on RacePosition {\n      position\n      payoutAmount\n      currency\n      race {\n        name\n        endTime\n      }\n    }\n    ... on CommunityMute {\n      active\n      message\n      expireAt\n    }\n    ... on ChallengeWin {\n      challenge {\n        ...Challenge\n      }\n    }\n    ... on Challenge {\n      ...Challenge\n    }\n    ... on NotificationFiatError {\n      code\n      limitType\n      fiatErrorAmount: amount\n      fiatErrorCurrency: currency\n    }\n    ... on VeriffUser {\n      veriffStatus: status\n      veriffReason: reason\n    }\n    ... on SportsbookPromotionBet {\n      id\n      bet {\n        id\n      }\n      betAmount\n      value\n      currency\n      payout\n      payoutValue\n      sportsbookPromotionBetStatus: status\n      sportsbookPromotionBetUser: user {\n        id\n        name\n      }\n      promotion {\n        id\n        name\n      }\n    }\n    ... on UserPostcardCode {\n      id\n      claimedAt\n      postcardCode: code\n    }\n  }\n}\n\nfragment SportMarket on SportMarket {\n  id\n  name\n  status\n  extId\n  specifiers\n  customBetAvailable\n  provider\n}\n\nfragment TournamentTree on SportTournament {\n  id\n  name\n  slug\n  category {\n    ...CategoryTree\n  }\n}\n\nfragment CategoryTree on SportCategory {\n  id\n  name\n  slug\n  sport {\n    id\n    name\n    slug\n  }\n}\n\nfragment SportFixtureDataMatch on SportFixtureDataMatch {\n  startTime\n  competitors {\n    ...SportFixtureCompetitor\n  }\n  teams {\n    name\n    qualifier\n  }\n  tvChannels {\n    language\n    name\n    streamUrl\n  }\n  __typename\n}\n\nfragment SportFixtureCompetitor on SportFixtureCompetitor {\n  name\n  extId\n  countryCode\n  abbreviation\n  iconPath\n}\n\nfragment SportFixtureDataOutright on SportFixtureDataOutright {\n  name\n  startTime\n  endTime\n  __typename\n}\n\nfragment SwishBetFragment on SwishBet {\n  __typename\n  active\n  amount\n  cashoutMultiplier\n  createdAt\n  currency\n  customBet\n  id\n  odds\n  payout\n  payoutMultiplier\n  updatedAt\n  status\n  user {\n    id\n    name\n    preferenceHideBets\n  }\n  outcomes {\n    __typename\n    id\n    odds\n    lineType\n    outcome {\n      ...SwishMarketOutcomeFragment\n    }\n  }\n}\n\nfragment SwishMarketOutcomeFragment on SwishMarketOutcome {\n  __typename\n  id\n  line\n  over\n  under\n  gradeOver\n  gradeUnder\n  suspended\n  balanced\n  name\n  competitor {\n    id\n    name\n  }\n  market {\n    id\n    stat {\n      name\n      value\n    }\n    game {\n      id\n      fixture {\n        id\n        name\n        slug\n        status\n        eventStatus {\n          ...SportFixtureEventStatus\n          ...EsportFixtureEventStatus\n        }\n        data {\n          ... on SportFixtureDataMatch {\n            __typename\n            startTime\n            competitors {\n              name\n              extId\n              countryCode\n              abbreviation\n            }\n          }\n        }\n        tournament {\n          id\n          slug\n          category {\n            id\n            slug\n            sport {\n              id\n              name\n              slug\n            }\n          }\n        }\n      }\n    }\n  }\n}\n\nfragment SportFixtureEventStatus on SportFixtureEventStatusData {\n  __typename\n  homeScore\n  awayScore\n  matchStatus\n  clock {\n    matchTime\n    remainingTime\n  }\n  periodScores {\n    homeScore\n    awayScore\n    matchStatus\n  }\n  currentTeamServing\n  homeGameScore\n  awayGameScore\n  statistic {\n    yellowCards {\n      away\n      home\n    }\n    redCards {\n      away\n      home\n    }\n    corners {\n      home\n      away\n    }\n  }\n}\n\nfragment EsportFixtureEventStatus on EsportFixtureEventStatus {\n  matchStatus\n  homeScore\n  awayScore\n  scoreboard {\n    homeGold\n    awayGold\n    homeGoals\n    awayGoals\n    homeKills\n    awayKills\n    gameTime\n    homeDestroyedTowers\n    awayDestroyedTurrets\n    currentRound\n    currentCtTeam\n    currentDefTeam\n    time\n    awayWonRounds\n    homeWonRounds\n    remainingGameTime\n  }\n  periodScores {\n    type\n    number\n    awayGoals\n    awayKills\n    awayScore\n    homeGoals\n    homeKills\n    homeScore\n    awayWonRounds\n    homeWonRounds\n    matchStatus\n  }\n  __typename\n}\n\nfragment Challenge on Challenge {\n  id\n  type\n  active\n  adminCreated\n  completedAt\n  award\n  claimCount\n  claimMax\n  currency\n  isRefunded\n  minBetUsd\n  betCurrency\n  startAt\n  expireAt\n  updatedAt\n  createdAt\n  targetMultiplier\n  game {\n    id\n    name\n    slug\n    thumbnailUrl\n  }\n  creatorUser {\n    ...UserTags\n  }\n  affiliateUser {\n    ...UserTags\n  }\n  wins {\n    id\n    claimedBy {\n      ...UserTags\n    }\n  }\n}\n\nfragment UserTags on User {\n  id\n  name\n  isMuted\n  isRainproof\n  isIgnored\n  isHighroller\n  isSportHighroller\n  leaderboardDailyProfitRank\n  leaderboardDailyWageredRank\n  leaderboardWeeklyProfitRank\n  leaderboardWeeklyWageredRank\n  flags {\n    flag\n    rank\n    createdAt\n  }\n  roles {\n    name\n    expireAt\n    message\n  }\n  createdAt\n  preferenceHideBets\n}\n",
                "variables": {
                    "limit": limit,
                    "offset": 0
                }
            },
            cookies={
                "cf_clearance": self.cf_clearance
            }
        ).json()

        return response
    
    def get_vip_progress(self):
        if self.api_key == None:
            raise StakePyError("APIキーの指定が必要です")

        response = self.session.post(
            "https://stake.com/_api/graphql",
            headers={
                "Content-Type": "application/json",
                "User-Agent": self.user_agent,
                "X-Access-Token": self.api_key
            },
            json={
                "operationName": "VipProgressMeta",
                "query": "query VipProgressMeta {\n  user {\n    id\n    flagProgress {\n      flag\n      progress\n      __typename\n    }\n    __typename\n  }\n}\n"
            },
            cookies={
                "cf_clearance": self.cf_clearance
            }
        ).json()

        return response
    
    def get_balances(self):
        if self.api_key == None:
            raise StakePyError("APIキーの指定が必要です")

        response = self.session.post(
            "https://stake.com/_api/graphql",
            headers={
                "Content-Type": "application/json",
                "User-Agent": self.user_agent,
                "X-Access-Token": self.api_key
            },
            json={
                "operationName": "UserBalances",
                "query": "query UserBalances {\n  user {\n    id\n    balances {\n      available {\n        amount\n        currency\n        __typename\n      }\n      vault {\n        amount\n        currency\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
            },
            cookies={
                "cf_clearance": self.cf_clearance
            }
        ).json()

        return response
    
    def get_deposit_address(self, currency: str = "ltc"):
        if self.api_key == None:
            raise StakePyError("APIキーの指定が必要です")

        response = self.session.post(
            "https://stake.com/_api/graphql",
            headers={
                "Content-Type": "application/json",
                "User-Agent": self.user_agent,
                "X-Access-Token": self.api_key
            },
            json={
                "operationName": "DepositAddress",
                "query": "query DepositAddress($chain: CryptoChainEnum, $currency: CryptoCurrencyEnum!, $type: WalletAddressType!, $infoCurrency: CurrencyEnum!) {\n  info {\n    currency(currency: $infoCurrency) {\n      requiredConfirmations\n      __typename\n    }\n    __typename\n  }\n  user {\n    id\n    depositAddress(chain: $chain, currency: $currency, type: $type) {\n      id\n      address\n      currency\n      __typename\n    }\n    __typename\n  }\n}\n",
                "variables": {
                    "currency": currency,
                    "infoCurrency": currency,
                    "type": "default"
                }
            },
            cookies={
                "cf_clearance": self.cf_clearance
            }
        ).json()

        return response
    
    def send_tip(self, stake_id: str, currency: str, amount: float, tfa_token: str) -> dict:
        if self.api_key == None:
            raise StakePyError("APIキーの指定が必要です")
        
        response = self.session.post(
            "https://stake.com/_api/graphql",
            headers={
                "Content-Type": "application/json",
                "User-Agent": self.user_agent,
                "X-Access-Token": self.api_key
            },
            json={
                "operationName": "SendTipMeta",
                "query": "query SendTipMeta($name: String) {\n  user(name: $name) {\n    id\n    name\n    __typename\n  }\n  self: user {\n    id\n    hasTfaEnabled\n    isTfaSessionValid\n    balances {\n      available {\n        amount\n        currency\n        __typename\n      }\n      vault {\n        amount\n        currency\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
                "variables": {
                    "name": stake_id
                }
            },
            cookies={
                "cf_clearance": self.cf_clearance
            }
        ).json()
        if response["data"]["user"] == None:
            raise StakePyError("存在しないStakeIDです")
        user_id = response["data"]["user"]["id"]
        
        response = self.session.post(
            "https://stake.com/_api/graphql",
            headers={
                "Content-Type": "application/json",
                "User-Agent": self.user_agent,
                "X-Access-Token": self.api_key
            },
            json={
                "operationName": "SendTip",
                "query": "mutation SendTip($userId: String!, $amount: Float!, $currency: CurrencyEnum!, $isPublic: Boolean, $chatId: String!, $tfaToken: String) {\n  sendTip(\n    userId: $userId\n    amount: $amount\n    currency: $currency\n    isPublic: $isPublic\n    chatId: $chatId\n    tfaToken: $tfaToken\n  ) {\n    id\n    amount\n    currency\n    user {\n      id\n      name\n      __typename\n    }\n    sendBy {\n      id\n      name\n      balances {\n        available {\n          amount\n          currency\n          __typename\n        }\n        vault {\n          amount\n          currency\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
                "variables": {
                    "userId": user_id,
                    "amount": amount,
                    "currency": currency,
                    "isPublic": False,
                    "chatId": "c65b4f32-0001-4e1d-9cd6-e4b3538b43ae",
                    "tfaToken": tfa_token
                }
            },
            cookies={
                "cf_clearance": self.cf_clearance
            }
        ).json()

        return response
    
    def get_user_meta(self, signup_code: bool = True) -> dict:
        if self.api_key == None:
            raise StakePyError("APIキーの指定が必要です")

        response = self.session.post(
            "https://stake.com/_api/graphql",
            headers={
                "Content-Type": "application/json",
                "User-Agent": self.user_agent,
                "X-Access-Token": self.api_key
            },
            json={
                "query": "query UserMeta($name: String, $signupCode: Boolean = false) {\n  user(name: $name) {\n    id\n    name\n    isMuted\n    isRainproof\n    isBanned\n    createdAt\n    campaignSet\n    selfExclude {\n      id\n      status\n      active\n      createdAt\n      expireAt\n    }\n    signupCode @include(if: $signupCode) {\n      id\n      code {\n        id\n        code\n      }\n    }\n  }\n}\n",
                "variables": {
                    "signupCode": signup_code
                }
            },
            cookies={
                "cf_clearance": self.cf_clearance
            }
        ).json()

        return response
    
    def get_email_meta(self) -> dict:
        if self.api_key == None:
            raise StakePyError("APIキーの指定が必要です")

        response = self.session.post(
            "https://stake.com/_api/graphql",
            headers={
                "Content-Type": "application/json",
                "User-Agent": self.user_agent,
                "X-Access-Token": self.api_key
            },
            json={
                "query": "query UserEmailMeta {\n  user {\n    ...UserEmailFragment\n  }\n}\n\nfragment UserEmailFragment on User {\n  id\n  email\n  hasEmailVerified\n  hasEmailSubscribed\n}\n",
                "variables": {}
            },
            cookies={
                "cf_clearance": self.cf_clearance
            }
        ).json()

        return response
    
    def get_phone_meta(self) -> dict:
        if self.api_key == None:
            raise StakePyError("APIキーの指定が必要です")

        response = self.session.post(
            "https://stake.com/_api/graphql",
            headers={
                "Content-Type": "application/json",
                "User-Agent": self.user_agent,
                "X-Access-Token": self.api_key
            },
            json={
                "query": "query UserPhoneMeta {\n  user {\n    ...UserPhoneFragment\n  }\n}\n\nfragment UserPhoneFragment on User {\n  id\n  phoneNumber\n  phoneCountryCode\n  hasPhoneNumberVerified\n}\n",
                "variables": {}
            },
            cookies={
                "cf_clearance": self.cf_clearance
            }
        ).json()

        return response
    
    def get_kyc_meta(self) -> dict:
        if self.api_key == None:
            raise StakePyError("APIキーの指定が必要です")
        
        response = self.session.post(
            "https://stake.com/_api/graphql",
            headers={
                "Content-Type": "application/json",
                "User-Agent": self.user_agent,
                "X-Access-Token": self.api_key
            },
            json={
                "query": "query UserKycInfo {\n  isDiscontinuedBlocked\n  user {\n    id\n    roles {\n      name\n    }\n    kycStatus\n    dob\n    createdAt\n    isKycBasicRequired\n    isKycExtendedRequired\n    isKycFullRequired\n    isKycUltimateRequired\n    hasEmailVerified\n    phoneNumber\n    hasPhoneNumberVerified\n    email\n    registeredWithVpn\n    isBanned\n    isSuspended\n    isSuspendedSportsbook\n    kycBasic {\n      ...UserKycBasic\n    }\n    kycExtended {\n      ...UserKycExtended\n    }\n    kycFull {\n      ...UserKycFull\n    }\n    kycUltimate {\n      ...UserKycUltimate\n    }\n    veriffStatus\n    jpyAlternateName: cashierAlternateName(currency: jpy) {\n      firstName\n      lastName\n    }\n    nationalId\n    outstandingWagerAmount {\n      currency\n      amount\n      progress\n    }\n    activeDepositBonus {\n      status\n    }\n    activeRollovers {\n      id\n      active\n      user {\n        id\n      }\n      amount\n      lossAmount\n      createdAt\n      note\n      currency\n      expectedAmount\n      expectedAmountMin\n      progress\n      activeBets {\n        id\n        iid\n        game {\n          id\n          slug\n          name\n        }\n        bet {\n          __typename\n        }\n      }\n    }\n  }\n}\n\nfragment UserKycBasic on UserKycBasic {\n  active\n  address\n  birthday\n  city\n  country\n  createdAt\n  firstName\n  id\n  lastName\n  phoneNumber\n  rejectedReason\n  status\n  updatedAt\n  zipCode\n  occupation\n}\n\nfragment UserKycExtended on UserKycExtended {\n  id\n  active\n  createdAt\n  id\n  rejectedReason\n  status\n}\n\nfragment UserKycFull on UserKycFull {\n  active\n  createdAt\n  id\n  rejectedReason\n  status\n}\n\nfragment UserKycUltimate on UserKycUltimate {\n  id\n  active\n  createdAt\n  id\n  rejectedReason\n  status\n}\n",
                "variables": {}
            },
            cookies={
                "cf_clearance": self.cf_clearance
            }
        ).json()

        return response