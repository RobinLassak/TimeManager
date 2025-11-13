using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ComponentModel.DataAnnotations;

namespace TimeManager.Domain
{
    public class BankAccountEntity : EntityBase
    {
        // Nazev uctu
        [Required, MaxLength(200)]
        public string Name { get; set; } = null!;


        // Vlastnik uctu
        [Required]
        public PersonEntity Owner { get; set; } = null!;


        // Predcisli uctu
        [MaxLength(6)]
        public string? AccountPrefix { get; set; }


        // Cislo uctu
        [Required, MaxLength(10)]
        public string AccountNumber { get; set; } = null!;


        // Kod banky
        [Required, MaxLength(4)]
        public string BankCode { get; set; } = null!;


        // Vazba na tabulku bank
        public int BankId { get; set; }
        public BankEntity Bank { get; set; } = null!;


        // IBAN
        [MaxLength(34)]
        public string? Iban { get; set; }


        // Jina banka nez domaci
        public bool IsOtherBank { get; set; }
        [MaxLength(200)] public string? OtherBankName { get; set; }
        [MaxLength(11)] public string? OtherBankCode { get; set; }
        [MaxLength(11)] public string? OtherBankBic { get; set; }
    }
}
