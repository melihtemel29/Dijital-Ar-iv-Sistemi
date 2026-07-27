import re

new_sdp = """SDP_KODLARI = {
    "000-099": {
        "name": "Ortak Kodlar",
        "departman_adi": "Tüm Birimler",
        "codes": {
            "010": {
                "title": "Kurullar ve Komisyonlar",
                "subcodes": {
                    "010.01": "Senato",
                    "010.02": "Yönetim Kurulu",
                    "010.03": "İhtisas Komisyonları",
                    "010.04": "Çalışma Grubu / Komisyonlar"
                }
            },
            "030": {
                "title": "Mevzuat İşleri",
                "subcodes": {
                    "030.01": "Kanun, Kanun Hükmünde Kararname",
                    "030.02": "Tüzük, Yönetmelik",
                    "030.03": "Yönerge, Usul ve Esaslar",
                    "030.04": "Genelge, Talimat, Senato Kararı"
                }
            },
            "040": {
                "title": "Faaliyet Raporları ve Brifingler",
                "subcodes": {
                    "040.01": "Faaliyet Raporları (Birim/Kurum)",
                    "040.02": "Brifingler"
                }
            },
            "050": {
                "title": "Genel Yazışmalar",
                "subcodes": {
                    "050.01": "Genel İşler ve Duyurular",
                    "050.02": "Görüş Talepleri ve Cevapları",
                    "050.06": "Bilgi Edinme İstekleri",
                    "050.99": "Diğer İşler"
                }
            }
        }
    },
    "300-399": {
        "name": "Akademik ve Eğitim Birimleri",
        "departman_adi": "Öğrenci İşleri Daire Başkanlığı",
        "codes": {
            "300": {
                "title": "Eğitim ve Öğretim İşleri (Genel)",
                "subcodes": {
                    "300.01": "Akademik Takvim",
                    "300.02": "Öğretim Yılı Hazırlıkları"
                }
            },
            "301": {
                "title": "Öğrenci Kontenjanları ve Kabul İşlemleri",
                "subcodes": {
                    "301.01": "Kontenjan Belirleme",
                    "301.02": "Özel Yetenek Sınavı ile Kabul",
                    "301.03": "Yabancı Uyruklu Öğrenci Kabulü"
                }
            },
            "302": {
                "title": "Öğrenci Kayıt İşleri ve Dosyaları",
                "subcodes": {
                    "302.01": "Yeni Kayıt İşlemleri",
                    "302.02": "Kayıt Yenileme / Ders Kaydı",
                    "302.03": "Kayıt Dondurma / Silme"
                }
            },
            "304": {
                "title": "Sınav ve Değerlendirme İşlemleri",
                "subcodes": {
                    "304.01": "Sınav Programları",
                    "304.02": "Mazeret / Tek Ders Sınavları",
                    "304.03": "Sınav Sonuçları ve İtirazlar"
                }
            },
            "308": {
                "title": "Mezuniyet ve Diploma İşlemleri",
                "subcodes": {
                    "308.01": "Mezuniyet Kararları / Dereceler",
                    "308.02": "Diploma ve Sertifika Basımı",
                    "308.03": "Diploma Eki ve Geçici Mezuniyet Belgesi"
                }
            },
            "310": {
                "title": "Yatay / Dikey Geçiş İşlemleri",
                "subcodes": {
                    "310.01": "Kurum İçi / Kurumlar Arası Yatay Geçiş",
                    "310.02": "Dikey Geçiş İşlemleri",
                    "310.03": "İntibak ve Muafiyet İşlemleri"
                }
            },
            "320": {
                "title": "Burs ve Sosyal Yardım İşlemleri",
                "subcodes": {
                    "320.01": "YKY / KYK Burs/Kredi İşlemleri",
                    "320.02": "Özel / Kurum Bursları",
                    "320.03": "Yemek, Barınma ve Destek Yardımları"
                }
            },
            "340": {
                "title": "Ders Programları ve Müfredat İşlemleri",
                "subcodes": {
                    "340.01": "Müfredat Düzenleme ve Güncelleme",
                    "340.02": "Haftalık Ders Programları",
                    "340.03": "Ders Görevlendirmeleri"
                }
            }
        }
    },
    "400-599": {
        "name": "Sağlık, Kültür ve Spor",
        "departman_adi": "Sağlık, Kültür ve Spor Daire Başkanlığı",
        "codes": {
            "410": {
                "title": "Kültürel Faaliyetler",
                "subcodes": {
                    "410.01": "Konser, Tiyatro, Sergi vb.",
                    "410.02": "Öğrenci Kulüpleri ve Toplulukları"
                }
            },
            "420": {
                "title": "Spor Faaliyetleri",
                "subcodes": {
                    "420.01": "Spor Turnuvaları ve Yarışmalar",
                    "420.02": "Tesis Kullanımı ve Takımlar"
                }
            },
            "430": {
                "title": "Beslenme ve Yemek Hizmetleri",
                "subcodes": {
                    "430.01": "Yemekhane İşletimi ve Menü",
                    "430.02": "Gıda Hijyen ve Denetimleri"
                }
            },
            "440": {
                "title": "Barınma Hizmetleri",
                "subcodes": {
                    "440.01": "Yurt / Konukevi Kayıt ve Tahsis",
                    "440.02": "Yurt İşletim İşlemleri"
                }
            },
            "450": {
                "title": "Sağlık Hizmetleri",
                "subcodes": {
                    "450.01": "Muayene ve Tedavi Hizmetleri",
                    "450.02": "Psikolojik Danışmanlık ve Rehberlik"
                }
            }
        }
    },
    "600-619": {
        "name": "Strateji ve Planlama",
        "departman_adi": "Strateji Geliştirme Daire Başkanlığı",
        "codes": {
            "020": {
                "title": "Kurumsal İstatistikler ve Veri Analizleri",
                "subcodes": {
                    "020.01": "Periyodik İstatistikler",
                    "020.02": "Anket ve Veri Toplama"
                }
            },
            "601": {
                "title": "Stratejik Planlama İşlemleri",
                "subcodes": {
                    "601.01": "Stratejik Plan Hazırlama",
                    "601.02": "İzleme ve Değerlendirme"
                }
            },
            "602": {
                "title": "Performans Programı ve Faaliyet Raporları",
                "subcodes": {
                    "602.01": "Performans Programı",
                    "602.02": "Kurumsal Faaliyet Raporu"
                }
            },
            "610": {
                "title": "İç Kontrol Sistemi Geliştirme Çalışmaları",
                "subcodes": {
                    "610.01": "Risk Yönetimi",
                    "610.02": "İş Süreçleri ve Görev Tanımları"
                }
            }
        }
    },
    "620-639": {
        "name": "Kütüphane",
        "departman_adi": "Kütüphane ve Dokümantasyon Daire Başkanlığı",
        "codes": {
            "622": {
                "title": "Kitap, Süreli Yayın ve Materyal Alımı",
                "subcodes": {
                    "622.01": "Yayın İstekleri ve Seçimi",
                    "622.02": "Bağış ve Değişim Yayınlar"
                }
            },
            "624": {
                "title": "Kataloglama ve Sınıflandırma İşlemleri",
                "subcodes": {
                    "624.01": "Kataloglama",
                    "624.02": "Etiketleme ve Ciltleme"
                }
            },
            "626": {
                "title": "Kütüphane Kullanım ve Ödünç Verme İşleri",
                "subcodes": {
                    "626.01": "Üye İşlemleri",
                    "626.02": "Ödünç Verme / İade / İkaz"
                }
            },
            "632": {
                "title": "Elektronik Veri Tabanı Abonelikleri",
                "subcodes": {
                    "632.01": "Veri Tabanı Talepleri",
                    "632.02": "Abonelik ve Kullanım İstatistikleri"
                }
            }
        }
    },
    "640-659": {
        "name": "Hukuk Müşavirliği",
        "departman_adi": "Hukuk Müşavirliği",
        "codes": {
            "641": {
                "title": "Adli ve İdari Davalar",
                "subcodes": {
                    "641.01": "İdari Davalar",
                    "641.02": "Adli Davalar"
                }
            },
            "645": {
                "title": "İcra Takipleri",
                "subcodes": {
                    "645.01": "Kurum Alacakları",
                    "645.02": "Borç Takibi"
                }
            },
            "651": {
                "title": "Hukuki Mütalaalar",
                "subcodes": {
                    "651.01": "Birimlerden Gelen Hukuki Görüş Talepleri",
                    "651.02": "Dış Kurumlara Verilen Görüşler"
                }
            }
        }
    },
    "700-719": {
        "name": "Bilgi İşlem",
        "departman_adi": "Bilgi İşlem Daire Başkanlığı",
        "codes": {
            "700": {
                "title": "Bilgi İşlem İşleri (Genel)",
                "subcodes": {
                    "700.01": "Bilgi İşlem Politikaları ve Standartları"
                }
            },
            "702": {
                "title": "Yazılım Geliştirme ve Proje İşlemleri",
                "subcodes": {
                    "702.01": "Yazılım Talepleri ve Analiz",
                    "702.02": "Proje Kodlama ve Test Süreçleri"
                }
            },
            "704": {
                "title": "Veri Tabanı ve Sunucu Yönetimi",
                "subcodes": {
                    "704.01": "Veri Tabanı Kurulum ve Yedekleme",
                    "704.02": "Sunucu Sanallaştırma ve Bakım"
                }
            },
            "708": {
                "title": "Donanım, Altyapı ve Ağ Yönetimi",
                "subcodes": {
                    "708.01": "Ağ (Network) Yapılandırması",
                    "708.02": "Donanım Envanter ve Dağıtım"
                }
            },
            "710": {
                "title": "Bilgi ve Siber Güvenlik İşlemleri",
                "subcodes": {
                    "710.01": "Güvenlik Duvarı (Firewall) ve Log Yönetimi",
                    "710.02": "Siber Olaylara Müdahale (SOME)"
                }
            },
            "713": {
                "title": "Teknik Servis ve Bakım Onarım İşlemleri",
                "subcodes": {
                    "713.01": "Arıza Bildirimleri",
                    "713.02": "Periyodik Donanım Bakımları"
                }
            }
        }
    },
    "750-769": {
        "name": "Yapı İşleri",
        "departman_adi": "Yapı İşleri ve Teknik Daire Başkanlığı",
        "codes": {
            "751": {
                "title": "Etüt-Proje ve Kamulaştırma İşleri",
                "subcodes": {
                    "751.01": "Mimari ve Mühendislik Projeleri",
                    "751.02": "Kamulaştırma İşlemleri"
                }
            },
            "755": {
                "title": "Yapım (İnşaat) İhaleleri ve Dosyaları",
                "subcodes": {
                    "755.01": "İnşaat İhale Dosyaları",
                    "755.02": "Hakediş ve Geçici/Kabul İşlemleri"
                }
            },
            "757": {
                "title": "Büyük Onarım ve Tadilat İşleri",
                "subcodes": {
                    "757.01": "Onarım Keşif ve Şartnameleri",
                    "757.02": "Tadilat Uygulamaları"
                }
            },
            "764": {
                "title": "Enerji, Isıtma ve Tesisat İşleri",
                "subcodes": {
                    "764.01": "Elektrik, Su, Doğalgaz Abonelikleri",
                    "764.02": "Tesisat Periyodik Bakımları"
                }
            }
        }
    },
    "840-869": {
        "name": "Mali İşler",
        "departman_adi": "İdari ve Mali İşler Daire Başkanlığı",
        "codes": {
            "841": {
                "title": "Bütçe Hazırlama ve Uygulama",
                "subcodes": {
                    "841.01": "Bütçe Çağrısı ve Hazırlıklar",
                    "841.02": "Bütçe Aktarma ve Revize İşlemleri"
                }
            },
            "843": {
                "title": "Ödenek İşlemleri",
                "subcodes": {
                    "843.01": "Ödenek Gönderme",
                    "843.02": "Tenkis İşlemleri"
                }
            },
            "851": {
                "title": "Muhasebe İşlemleri",
                "subcodes": {
                    "851.01": "Yıl Sonu Hesap Kapama",
                    "851.02": "Mutabakat Belgeleri"
                }
            },
            "855": {
                "title": "Ödeme İşlemleri",
                "subcodes": {
                    "855.01": "Maaş, Ücret ve Yolluk Ödemeleri",
                    "855.02": "Fatura Ödeme Evrakı (Mevzuat/Mal/Hizmet)"
                }
            },
            "869": {
                "title": "Taşınır Mal İşlemleri",
                "subcodes": {
                    "869.01": "Taşınır Giriş / Çıkış (TİF)",
                    "869.02": "Sayım, Düşüm ve Hurda İşlemleri"
                }
            }
        }
    },
    "900-929": {
        "name": "Personel İşleri",
        "departman_adi": "Personel Daire Başkanlığı",
        "codes": {
            "900": {
                "title": "Personel İşleri (Genel)",
                "subcodes": {
                    "900.01": "Personel Politikaları ve İstatistikleri"
                }
            },
            "901": {
                "title": "Kadro İşlemleri",
                "subcodes": {
                    "901.01": "Kadro İhdası ve İptali",
                    "901.02": "Kadro Dağılımı ve Kullanımı"
                }
            },
            "902": {
                "title": "Atama ve Görevlendirme İşleri",
                "subcodes": {
                    "902.01": "Açıktan / Naklen Atamalar",
                    "902.02": "Vekalet ve İkinci Görev"
                }
            },
            "903": {
                "title": "Personel Özlük İşleri",
                "subcodes": {
                    "903.01": "İşe Giriş Belgeleri",
                    "903.02": "Atama İşleri",
                    "903.03": "Terfi ve İntibak İşleri",
                    "903.04": "Hizmet Cetveli ve Hizmet Belgesi",
                    "903.05": "Personel İzin İşlemleri",
                    "903.06": "Görevden Ayrılma",
                    "903.07": "Görevlendirme"
                }
            },
            "907": {
                "title": "Disiplin ve Cezai İşlemler",
                "subcodes": {
                    "907.01": "Disiplin Soruşturmaları",
                    "907.02": "Disiplin Cezaları ve İtirazlar"
                }
            },
            "915": {
                "title": "Sendikal Faaliyetler",
                "subcodes": {
                    "915.01": "Sendika Üyelik / İstifa",
                    "915.02": "Toplu Sözleşme İşlemleri"
                }
            },
            "918": {
                "title": "Emeklilik İşlemleri",
                "subcodes": {
                    "918.01": "Yaş Haddi / İsteğe Bağlı Emeklilik",
                    "918.02": "Malulen Emeklilik"
                }
            }
        }
    },
    "930-949": {
        "name": "Satın Alma ve İhale",
        "departman_adi": "İdari ve Mali İşler Daire Başkanlığı",
        "codes": {
            "930": {
                "title": "Satın Alma ve İhale İşleri (Genel)",
                "subcodes": {
                    "930.01": "Satın Alma Talepleri"
                }
            },
            "934": {
                "title": "İhale İşlemleri",
                "subcodes": {
                    "934.01": "Açık İhale Usulü Dosyaları",
                    "934.02": "Pazarlık Usulü İhale Dosyaları",
                    "934.03": "İhale Komisyon Kararları"
                }
            },
            "942": {
                "title": "Piyasa Fiyat Araştırması",
                "subcodes": {
                    "942.01": "Fiyat Teklif Formları",
                    "942.02": "Yaklaşık Maliyet Cetvelleri"
                }
            },
            "944": {
                "title": "Doğrudan Temin İşlemleri",
                "subcodes": {
                    "944.01": "Doğrudan Temin Onay Belgeleri",
                    "944.02": "Fatura ve Alım Belgeleri"
                }
            }
        }
    }
}
"""

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find SDP_KODLARI using regex
# Match SDP_KODLARI = { ... } (including newlines) until the next @app.route or similar root level statement
pattern = re.compile(r'SDP_KODLARI\s*=\s*\{.*?\n\}\n', re.DOTALL)
match = pattern.search(content)

if match:
    new_content = content[:match.start()] + new_sdp + "\n\n" + content[match.end():]
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SDP_KODLARI replaced successfully.")
else:
    print("Could not find SDP_KODLARI block.")
